import json

inputfile = '/root/adaseq/experiments/globalpoter/241107212922.633395/pred.json'
with open(inputfile, 'r', encoding='utf-8') as file:
    for line in file:
        data = json.loads(line.strip())
        tokens = data.get('tokens', [])
        spans = data.get('spans', [])
        predicts = data.get('predicts', [])

        for span in spans:
            start = span.get('start')
            end = span.get('end')
            span_type = span.get('type')
            
            if start is not None and end is not None and start < len(tokens) and end <= len(tokens):
                span_tokens = tokens[start:end]
                span['word'] = span_tokens
        for predict in predicts:
            start = predict[0]
            end = predict[1]
            predict_type = predict[2]

            if start is not None and end is not None and start < len(tokens) and end <= len(tokens):
                predict_tokens = tokens[start:end]
                predict.append(predict_tokens)


        # print(json.dumps(data, ensure_ascii=False))
        outputfile = "/root/data/outputs/predict.json"
        with open(outputfile, 'a', encoding='utf-8') as output_file:
            for key, value in data.items():
                output_file.write(f"{key}: {json.dumps(value, ensure_ascii=False)}\n")
            output_file.write("\n")

print("finished")

