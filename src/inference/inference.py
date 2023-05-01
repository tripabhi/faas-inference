from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import os
import pathutil

output_map = {1: 'Negative', 2: 'Neutral', 3: 'Positive', 4: 'Very Positive', 5: 'Very Negative'}

_data_path = pathutil.get_data_path()

modelname = os.path.join(_data_path, 'model_sentiment.pt')
tokenname = os.path.join(_data_path, 'tokenizer_sentiment.pt')
model = AutoModelForSequenceClassification.from_pretrained(modelname)
tokenizer = AutoTokenizer.from_pretrained(tokenname)

def infer(data):
    tokens = tokenizer.encode(data, return_tensors='pt')
    result = model(tokens)
    return output_map[int(torch.argmax(result.logits))+1]
