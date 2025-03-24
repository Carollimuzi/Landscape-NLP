import json

# predfile = "/root/cjr/projects/adaseq/experiments/distilBERT/241102182853.614048/pred.txt"
predfile = input("the path of pred.txt from model:")
with open(predfile, 'r') as file:
    lines = file.readlines()
data = [json.loads(line) for line in lines]

max_token_length = 0
max_label_length = 0
max_predict_length = 0

for entry in data:
    tokens = entry['tokens']
    labels = entry['labels']
    predicts = entry['predicts']
    
    max_token_length = max(max_token_length, max(len(tokens) for token in tokens))
    max_label_length = max(max_label_length, max(len(label) for label in labels))
    max_predict_length = max(max_predict_length, max(len(predict) for predict in predicts))
    max_length = max( max_label_length, max_predict_length)

formatted_lines = []
for entry in data:
    tokens = ''.join(token.ljust(max_length) for token in entry['tokens'])
    labels = ''.join(label.ljust(max_length) for label in entry['labels'])
    predicts = ''.join(predict.ljust(max_length) for predict in entry['predicts'])
    
    formatted_lines.append(f"tokens: {tokens}\nlabels: {labels}\npreds:  {predicts}\n \n")

outname = input("saving name: ")
output = "/root/cjr/data/outputs/" + outname
with open(output, 'w') as file:
    file.writelines(formatted_lines)

print("finished")
