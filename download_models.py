
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import os
import logging
import pathutil

logging.basicConfig(format='%(asctime)s - %(message)s')

def download_models():
    __path = pathutil.get_data_path()
    tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
    model = AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
    tokenizer.save_pretrained(f'{__path}/tokenizer_sentiment.pt')
    model.save_pretrained(f'{__path}/model_sentiment.pt')
    


download_models()