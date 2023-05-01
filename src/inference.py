from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import os

'''
code to download the model and tokenizer
tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')

model = AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')

tokens = tokenizer.encode('It was good but couldve been better. Great', return_tensors='pt')

result = model(tokens)


int(torch.argmax(result.logits))+1
tokenizer.save_pretrained('tokenizer_sentiment.pt')
model.save_pretrained('model_sentiment.pt')
'''


output_map = {1: 'Negative', 2: 'Neutral', 3: 'Positive', 4: 'Very Positive', 5: 'Very Negative'}


dirname = os.path.dirname(__file__)
modelname = os.path.join(dirname, 'model_sentiment.pt')
tokenname = os.path.join(dirname, 'tokenizer_sentiment.pt')
model = AutoModelForSequenceClassification.from_pretrained(modelname)
tokenizer = AutoTokenizer.from_pretrained(tokenname)


def infer(data):
    tokens = tokenizer.encode(data, return_tensors='pt')
    result = model(tokens)
    return output_map[int(torch.argmax(result.logits))+1]
