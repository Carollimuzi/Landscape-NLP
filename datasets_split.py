import csv
import json
import os
import random
import pandas as pd
from collections import defaultdict


def csv_to_custom_json_single_split(input_csv_path, mapping_csv_path, seed: int = 42):
    """
    Convert CSV to JSONL (train/valid/test) using a single split by park.
    Also output:
      - {input_filename}.json  (train+valid+test)
      - {input_filename}_validtrain.json (train+valid)
    """
    random.seed(seed)
    input_dir = os.path.dirname(os.path.abspath(input_csv_path))
    input_filename = os.path.splitext(os.path.basename(input_csv_path))[0]

    # === 1 ===
    df_map = pd.read_csv(mapping_csv_path, usecols=["ID", "SourceFile"])
    df_map["SourceFile"] = df_map["SourceFile"].apply(
        lambda x: os.path.splitext(os.path.basename(str(x).strip()))[0]
    )
    id_to_park = {str(k).strip().lower(): v for k, v in zip(df_map["ID"], df_map["SourceFile"])}

    # === 2 ===
    samples, sample, spans = [], {}, []
    text_line_read = False

    with open(input_csv_path, "r", newline="", encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            if not any(row):
                continue
            if not text_line_read:
                text = []
                for i, word in enumerate(row):
                    if word or (i < len(row) - 1 and row[i + 1]):
                        text.append(word)
                sample['text'] = text
                text_line_read = True
                continue
            if row[0] != "#ID":
                start, end, span_type = None, None, None
                for idx, cell in enumerate(row):
                    if cell != "":
                        if start is None:
                            start = idx
                        end = idx + 1
                        span_type = cell
                if start is not None and span_type is not None:
                    spans.append({"start": start, "end": end, "type": span_type})
            else:
                sid = str(row[1]).strip().lower()
                park = id_to_park.get(sid, "unknown")
                sample["id"] = sid
                sample["spans"] = spans
                sample["park"] = park
                samples.append(sample)
                sample, spans, text_line_read = {}, [], False

    samples = [s for s in samples if s["spans"]]
    total_samples = len(samples)
    print(f"[INFO] Total samples: {total_samples}")

    # === 3 ===
    park2idxs = defaultdict(list)
    for i, s in enumerate(samples):
        park2idxs[s["park"]].append(i)
    park_sizes = [(p, len(idxs)) for p, idxs in park2idxs.items()]
    park_sizes.sort(key=lambda x: x[1], reverse=True)
    parks = [p for p, _ in park_sizes]
    random.shuffle(parks)

    # === 4 ===
    total = sum(len(idxs) for idxs in park2idxs.values())
    cum_sum = 0
    train_parks, valid_parks, test_parks = [], [], []

    for p in parks:
        cum_sum += len(park2idxs[p])
        ratio = cum_sum / total
        if ratio <= 0.7:
            train_parks.append(p)
        elif ratio <= 0.8:
            valid_parks.append(p)
        else:
            test_parks.append(p)

    if not valid_parks and test_parks:
        valid_parks.append(test_parks.pop(0))
    if not train_parks:
        train_parks.append(valid_parks.pop(0))

    # === 5 ===
    train_samples = [s for s in samples if s["park"] in train_parks]
    valid_samples = [s for s in samples if s["park"] in valid_parks]
    test_samples = [s for s in samples if s["park"] in test_parks]

    def write_jsonl(path, data):
        kept = 0
        with open(path, "w", encoding="utf-8") as f:
            for s in data:
                f.write(json.dumps(s, ensure_ascii=False) + "\n")
                kept += 1
        print(f"[INFO] Wrote {kept} samples to {os.path.basename(path)}")

    train_path = os.path.join(input_dir, f"{input_filename}_train.json")
    valid_path = os.path.join(input_dir, f"{input_filename}_valid.json")
    test_path = os.path.join(input_dir, f"{input_filename}_test.json")
    validtrain_path = os.path.join(input_dir, f"{input_filename}_validtrain.json")
    all_path = os.path.join(input_dir, f"{input_filename}.json")

    print("\n===== Split Summary =====")
    print(f"Train: {len(train_samples)} | Valid: {len(valid_samples)} | Test: {len(test_samples)}")

    # 写出文件
    write_jsonl(train_path, train_samples)
    write_jsonl(valid_path, valid_samples)
    write_jsonl(test_path, test_samples)
    write_jsonl(validtrain_path, train_samples + valid_samples)
    write_jsonl(all_path, train_samples + valid_samples + test_samples)

    print("\n Generated combined files:")
    print(f"→ {os.path.basename(validtrain_path)} (train+valid)")
    print(f"→ {os.path.basename(all_path)} (train+valid+test)")

    return validtrain_path

# =============================================================
# 5-fold GroupKFold by park
# =============================================================
def json_to_groupkfold_by_park(input_json_path, seed: int = 42):
    random.seed(seed)
    input_dir = os.path.dirname(os.path.abspath(input_json_path))
    input_filename = os.path.splitext(os.path.basename(input_json_path))[0]

    samples = []
    with open(input_json_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                samples.append(json.loads(line))
    total_samples = len(samples)
    print(f"[INFO] Loaded {total_samples} samples from {input_json_path}")

    park2idxs = defaultdict(list)
    for i, s in enumerate(samples):
        park2idxs[s["park"]].append(i)
    park_sizes = [(p, len(idxs)) for p, idxs in park2idxs.items()]
    park_sizes.sort(key=lambda x: x[1], reverse=True)

    folds = [{"parks": [], "size": 0} for _ in range(5)]
    for park, sz in park_sizes:
        tgt = min(range(5), key=lambda i: folds[i]["size"])
        folds[tgt]["parks"].append(park)
        folds[tgt]["size"] += sz

    total = sum(f["size"] for f in folds)
    print("\n===== Fold Sample Distribution =====")
    for i, f in enumerate(folds, 1):
        ratio = f["size"] / total * 100
        print(f"Fold {i}: {f['size']} samples ({ratio:.1f}%) | {len(f['parks'])} parks")

    def write_jsonl(path, data):
        with open(path, "w", encoding="utf-8") as f:
            for s in data:
                f.write(json.dumps(s, ensure_ascii=False) + "\n")
        print(f"[INFO] Wrote {len(data)} → {os.path.basename(path)}")

    for fold_i, fold in enumerate(folds, 1):
        valid_parks = set(fold["parks"])
        valid_idx = [i for i, s in enumerate(samples) if s["park"] in valid_parks]
        train_idx = [i for i, s in enumerate(samples) if s["park"] not in valid_parks]

        train_samples = [samples[i] for i in train_idx]
        valid_samples = [samples[i] for i in valid_idx]

        train_path = os.path.join(input_dir, f"{input_filename}_train_fold{fold_i}.json")
        valid_path = os.path.join(input_dir, f"{input_filename}_valid_fold{fold_i}.json")

        print(f"\n===== Fold {fold_i} =====")
        print(f"Train: {len(train_samples)} | Valid: {len(valid_samples)}")
        write_jsonl(train_path, train_samples)
        write_jsonl(valid_path, valid_samples)

        overlap = {s["park"] for s in train_samples} & {s["park"] for s in valid_samples}
        if overlap:
            print(f"⚠ Overlap parks detected: {overlap}")
        else:
            print(" No overlap between parks (perfect group split)")

    print("\nGroupKFold-style 5-fold split completed successfully!")

if __name__ == "__main__":
    input_csv = "home/AdaSeq-master/steps/fold/20250625data08.csv"
    mapping_csv = "home/AdaSeq-master/preprocessing/GMTA_source.csv"

    validtrain_path = csv_to_custom_json_single_split(input_csv, mapping_csv, seed=42)
    json_to_groupkfold_by_park(validtrain_path, seed=44)
