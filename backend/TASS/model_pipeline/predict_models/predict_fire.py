import io
from PIL import Image
from ultralytics import YOLO
import base64
import helpers
import asyncio

class Predict_Fire:
    __image = None
    __model_path = None
    __loop = asyncio.new_event_loop()
    def __init__(self, model_path):
        asyncio.set_event_loop(self.__loop)
        self.__model_path = model_path     
    
    def __load_model(self):
        model = YOLO(self.__model_path,) 
        return model
    
    def predict(self, key, db_data):
        model = self.__load_model()
        print('fire model loaded')
        # documents = []
        for doc in db_data:
            try:
                img = Image.open(io.BytesIO(base64.b64decode(doc['file_content'])))
                output = model(img, verbose=False)
            
                for result in output:
                    # print(result.boxes)
                    for box in result.boxes:
                        class_id = int(box.cls[0])
                        # print('class id: ', class_id)
                        # class_name = result.names[class_id]
                        
                        # if 'fire' in class_name:
                            # print(class_name, doc['file_name'])
                        document={'file_content': doc['file_content'],
                                    'file_name': doc['file_name']
                        }
                        print('documetn created')
                        # helpers.write_docs(key, document)
                        helpers.write_docs(key, document,self.__loop)
                            # collection.insert_one(document)
                        break
            except Exception as e:
                print("Corrupted: ",e)
        # helpers.write_docs(key, documents)

                
                        