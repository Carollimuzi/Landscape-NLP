import yaml
import csv
import json
import os

def update_config(config_path, train_file, valid_file, test_file):
    """
    update config file with train, valid, and test file paths
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file {config_path} not found.")
    with open(config_path, "r") as file:
        config = yaml.safe_load(file) or {} 

    if "dataset" not in config:
        config["dataset"] = {}
    if "data_file" not in config["dataset"]:
        config["dataset"]["data_file"] = {}
    config["dataset"]["data_file"]["train"] = train_file
    config["dataset"]["data_file"]["valid"] = valid_file
    config["dataset"]["data_file"]["test"] = test_file
    with open(config_path, "w") as file:
        yaml.dump(config, file, default_flow_style=False)
    print(f"Updated config file: {os.path.abspath(config_path)}")  

import random

def csv_to_custom_json(input_csv_path):
    """
    Converts a CSV file into target JSON format and splits it into train and test sets (4:1 ratio).

    - Automatically generates output JSON files in the same directory as input CSV.
    - Returns absolute paths of train.json and test.json.

    Example:
    Input CSV:
        hello, world, this, is, a, test
        , , , , , B-ENTITY
        #ID, sample_1

    Output JSON:
        train.json (80% of data)
        test.json (20% of data)
    """
    input_dir = os.path.dirname(os.path.abspath(input_csv_path))
    input_filename = os.path.splitext(os.path.basename(input_csv_path))[0]
    train_json_path = os.path.join(input_dir, f"{input_filename}_train.json")
    test_json_path = os.path.join(input_dir, f"{input_filename}_test.json")

    with open(input_csv_path, 'r', newline='', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        samples = []
        sample = {}
        spans = []
        text_line_read = False
        for row in reader:
            if not any(row):  
                continue
            if not text_line_read:
                text = [word for word in row if word]  
                sample['text'] = text
                text_line_read = True
                continue
            if row[0] != '#ID':
                start = None
                end = None
                span_type = None
                for idx, cell in enumerate(row):
                    if cell != '':
                        if start is None:
                            start = idx
                        end = idx + 1
                        span_type = cell
                if start is not None and span_type is not None:
                    spans.append({"start": start, "end": end, "type": span_type})
            elif row[0] == '#ID':
                sample['id'] = row[1]
                sample['spans'] = spans
                samples.append(sample)
                sample = {}
                spans = []
                text_line_read = False


    random.shuffle(samples)


    split_idx = int(len(samples) * 0.8)  # 80% for train, 20% for test, no validation set
    train_samples = samples[:split_idx]
    test_samples = samples[split_idx:]
    with open(train_json_path, 'w', encoding='utf-8') as train_file:
        for sample in train_samples:
            if sample['spans']:  
                train_file.write(json.dumps(sample, ensure_ascii=False) + '\n')

    with open(test_json_path, 'w', encoding='utf-8') as test_file:
        for sample in test_samples:
            if sample['spans']:  
                test_file.write(json.dumps(sample, ensure_ascii=False) + '\n')

    return train_json_path, test_json_path  
