import io
from PIL import Image
import base64
from pymongo import MongoClient
import helpers
import asyncio

class Predict_Nudity:
    __image = None
    __loop = asyncio.new_event_loop()
    def __init__(self):
        asyncio.set_event_loop(self.__loop)    
               

    def predict(self, key, db_data):

        from models.nudenet import NudeDetector

        nude_detector = NudeDetector()
        labels = [
            "BUTTOCKS_EXPOSED",
            "FEMALE_BREAST_EXPOSED",
            "FEMALE_GENITALIA_EXPOSED",
            "MALE_BREAST_EXPOSED",
            "ANUS_EXPOSED",
            "BELLY_EXPOSED",
            "MALE_GENITALIA_EXPOSED",
        ]
        # documents = []
        for doc in db_data:
                try:
                    print(doc['file_name'])
                    try:
                        output = nude_detector.detect(Image.open(io.BytesIO(base64.b64decode(doc['file_content']))))
                        for item in output:
                            if item["class"] in labels and item["score"] > 0.5:
                                censor_image = nude_detector.censor(Image.open(io.BytesIO(base64.b64decode(doc['file_content']))))
                                # img_low = io.BytesIO(Image.fromarray(censor_image))
                                document = {
                                    'censored_image': censor_image,
                                    'uncensored_image': doc['file_content'],
                                    'file_name': doc['file_name']
                                }
                                helpers.write_docs(key, document, self.__loop)
                                # collection.insert_one(document)
                                break
                    except (ValueError, IOError):
                        print(f"Error processing image: {doc['file_name']}")
                        continue
                except Exception as e:
                    print("Corrupted: ",e)
        # helpers.write_docs(key, documents)
