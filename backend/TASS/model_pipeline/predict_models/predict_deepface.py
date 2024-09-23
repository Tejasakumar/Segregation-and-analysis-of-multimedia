import cv2
import face_recognition
from pymongo import MongoClient
from PIL import Image
import dlib
import base64
import numpy as np




# client = MongoClient('mongodb://localhost:27017/')
# db = client['Carved_Files']
# db1 = client['ML_Files']
# collection_name = 'Faces'
# col1 = db1['Faces']


class Predict_DeepFace:
    __primary_string = "mongodb://localhost:27017/?readPreference=primary&replicaSet=rs0"
    __client = MongoClient(__primary_string)
    __faces = __client["Faces"]
    def __init__(self) -> None:
        pass

    def __check_match(self, face_1_encoding, face_2_encoding):
        return face_recognition.face_distance([face_1_encoding], face_2_encoding)[0] < 0.5

    def __detect_faces(image):
        detector = dlib.get_frontal_face_detector()  
        returns = detector(image)
        face_locations = face_recognition.face_locations(image)
        if len(returns)>0:
            return returns,"DLIB"
        elif len(face_locations)>0:
            return face_locations,"FR"
        else:
            return [],None
    
    def __save_faces(self, image_np, bboxes, content, type_det):
        for box in bboxes:
            if type_det=="DLIB":
                x1, y1, x2, y2 = box.left(), box.top(), box.right(), box.bottom()
                roi = image_np[y1:y2, x1:x2]
            elif type_det == "FR":
                y2, x2, y1, x1 = box
                roi = image_np[y2:y1, x1:x2]
            
            if len(roi)>0:
                try:
                    roi_rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
                except:
                    continue
            else:
                roi_rgb = image_np
            
            face_encoding = face_recognition.face_encodings(roi_rgb)
            if len(face_encoding) > 0:
                face1 = face_encoding[0]
            else:
                continue  
            
            list_of_collections = self.__faces.list_collection_names()

            if list_of_collections == []:
                collection_name = 'Face_1'
                self.__faces.create_collection(collection_name)
                document = {
                    'file_content': content,
                    'face': [x1, y1, x2, y2],
                    'type': type_det  
                }
                col1 = self.__faces[collection_name]
                col1.insert_one(document)
                continue

            else:  
                list_of_collections = sorted(list_of_collections)
                saved = False
                for col in list_of_collections:
                    print(col)
                    existing_documents = list(self.__faces[col].find({}))
                    count = 0
                    for doc in existing_documents:
                        dbimg_data = base64.b64decode(doc['file_content'])
                        dbimg_np = cv2.imdecode(np.frombuffer(dbimg_data, np.uint8), cv2.IMREAD_COLOR)
                        if doc['type']=='DLIB':
                            c1,c2,c3,c4 = doc['face']
                            dbimg_roi = dbimg_np[c2:c4, c1:c3]
                        elif doc['type']=='FR':
                            c4, c3, c2, c1 = doc['face']
                            dbimg_roi = dbimg_np[c4:c2, c1:c3]
                        dbimg_rgb = cv2.cvtColor(dbimg_roi, cv2.COLOR_BGR2RGB)
                        if len(face_recognition.face_encodings(dbimg_rgb))>0:
                            dbf_encoding = face_recognition.face_encodings(dbimg_rgb)[0]
                            if self.__check_match(face1,dbf_encoding):
                                count+=1
                                if(count>=self.__faces[col].count_documents({})/2):
                                    document = {
                                        'file_content': content,
                                        'face': [x1, y1, x2, y2],
                                        'type': type_det
                                    }
                                    col1 = self.__faces[col]
                                    col1.insert_one(document)
                                    saved = True
                                    break 
                        
                    if(count>=self.__faces[col].count_documents({})/2):
                        document = {
                            'file_content': content,
                            'face': [x1, y1, x2, y2],
                            'type': type_det  
                        }
                        col1 = self.__faces[col]
                        col1.insert_one(document)
                        saved = True
                        break    
                
                if not saved:
                    print(len(list_of_collections))
                    i = len(list_of_collections)+1
                    collection_name = f"Face_{i}"
                    document = {
                        'file_content': content,
                        'face': [x1, y1, x2, y2],
                        'type': type_det  
                    }
                    self.__faces[collection_name].insert_one(document)

    def predict(self, key, db_data):
        for doc in db_data:
            if 'file_content' in doc:
                image_data = base64.b64decode(doc['file_content'])
                image_np = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)
                image_rgb = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
                bboxes, type_det = self.__detect_faces(image_rgb)
                if bboxes:
                    self.__save_faces(image_np, bboxes, doc['file_content'], type_det)

