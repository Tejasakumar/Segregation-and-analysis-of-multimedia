        
import requests
from transformers import pipeline
import torch
import asyncio
import helpers
import yaml


class Predict_Llava:
    __loop = asyncio.new_event_loop()
    __classifier = None
    def __init__(self) -> None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print("llava",device)
        # classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli", device=device)
        self.classifier = pipeline("zero-shot-classification", model="MoritzLaurer/mDeBERTa-v3-base-mnli-xnli",device=device)
        asyncio.set_event_loop(self.__loop)

    def __classify(self, keys, text):
        result = self.classifier(text, keys, multi_label=True)
        keywords = [label for label, score in zip(result['labels'], result['scores']) if score > 0.85]
        return keywords

    def predict(self, keys, db_data):
        for doc in db_data:
            with open('data.yaml', 'r') as file:
                yaml_data = yaml.safe_load(file)
            port = yaml_data['ollama']['port']
            url = f"http://127.0.0.1:{port}/api/generate"
            
            keys_string = ', '.join(keys)
            prompt = f"Describe the image in one line"
            data = {
                "model": "llava",
                "prompt": prompt,
                "images": [doc['file_content']],
                "stream": False,
                "keep_alive" : 3600
            }
            response = requests.post(url, json=data)
            if response.status_code == 200:
                print(doc['file_name'])
                text = response.json().get('response')
                print(text)
                text_class = self.__classify(keys, text)
                print(text_class)
                for key in text_class:
                    helpers.write_llava_docs(key, doc, self.__loop)

            else:
                print(f"Request failed with status code: {response.status_code}")
