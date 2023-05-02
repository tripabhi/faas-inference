from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import os
import time
import json

output_map = {1: 'Very Negative', 2: 'Negative', 3: 'Neutral', 4: 'Positive', 5: 'Very Positive'}

dirname = os.path.dirname(__file__)
modelname = os.path.join(dirname, 'model_sentiment.pt')
tokenname = os.path.join(dirname, 'tokenizer_sentiment.pt')

time_model_load_start = time.monotonic()
model = AutoModelForSequenceClassification.from_pretrained(modelname)
tokenizer = AutoTokenizer.from_pretrained(tokenname)
time_model_load_end = time.monotonic()


def convert_to_ms(num):
    return int(round(num*1000))

def infer(data):
    t_start = time.monotonic()
    tokens = tokenizer.encode(data, return_tensors='pt')
    t_token = time.monotonic()
    result = model(tokens)
    t_inference = time.monotonic()
    value = {}
    value["TokenTime"] = convert_to_ms(t_token - t_start)
    value["InferenceTime"] = convert_to_ms(t_inference - t_token)
    value["TotalTime"] = convert_to_ms(t_inference - t_start)
    value["ModelLoadTime"] = convert_to_ms(time_model_load_end - time_model_load_start)
    value["data"] = output_map[int(torch.argmax(result.logits))+1]
    return json.dumps(value)
