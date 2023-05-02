#!/usr/bin/env python3
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import os
import logging


logging.basicConfig(format='%(asctime)s - %(message)s')

def download_models():
    dirname = os.path.dirname(__file__)
    modelname = os.path.join(dirname, 'src/inference/model_sentiment.pt')
    tokenname = os.path.join(dirname, 'src/inference/tokenizer_sentiment.pt')
    
    tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
    model = AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
    tokenizer.save_pretrained(tokenname)
    model.save_pretrained(modelname)
    


download_models()