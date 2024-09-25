from pymongo import MongoClient

# class DbReader:
    
#     MONGO_URI = 'mongodb://localhost:27017/?readPreference=primary&replicaSet=rs0'
#     client = MongoClient(MONGO_URI)
#     db = client["Carved_Files"]

#     def run(self, socketio):
#         print("in run")
#         self.retrive_one_doc(socketio)

#     def retrive_one_doc(self, socketio):
#         collections = self.db.list_collection_names()
#         for collection in collections:
#             coll = self.db[collection]
#             doc = coll.find_one()  # Retrieve one document
#             if doc:  # Ensure that a document was found
#                 file_content_binary = doc.get('file_content')
#                 file_name = doc.get('file_name')
#                 identity = str(doc.get('_id'))
#                 print("type", identity)

#                 # Assuming file_content_binary is already in a suitable format
#                 image_data = f"data:image;base64,{file_content_binary}"

#                 socketio.emit('image_name', {
#                     'content': {"data": image_data,
#                                 "id": identity},
#                     'folder': f"{collection}"
#                 })




class DbReader_Ml:
    MONGO_URI = 'mongodb://localhost:27017'
    client = MongoClient(MONGO_URI)
    db = client["ML_Files"]

    def run(self, socketio):
        print("in run")
        self.retrive_one_doc(socketio)

    def retrive_one_doc(self, socketio):
        collections = self.db.list_collection_names()
        for collection in collections:
            if collection != "Nudity":
                coll = self.db[collection]
                doc = coll.find_one()  # Retrieve one document
                if doc:  # Ensure that a document was found
                    file_content_binary = doc.get('file_content')
                    file_name = doc.get('file_name')
                    identity = str(doc.get('_id'))
                    print("type", identity)

                    # Assuming file_content_binary is already in a suitable format
                    image_data = f"data:image;base64,{file_content_binary}"

                    socketio.emit('image_name', {
                        'content': {"data": image_data,
                                    "id": identity},
                        'folder': f"{collection}"
                    })
class DbReader:
    
    MONGO_URI = 'mongodb://localhost:27017/?readPreference=primary&replicaSet=rs0'
    client = MongoClient(MONGO_URI)
    db = client["Carved_Files"]

    def run(self, socketio):
        print("in run")
        self.retrive_one_doc(socketio)

    def retrive_one_doc(self, socketio):
        collections = self.db.list_collection_names()
        for collection in collections:
            coll = self.db[collection]
            doc = coll.find_one()  # Retrieve one document
            if doc:  # Ensure that a document was found
                file_content_binary = doc.get('file_content')
                file_name = doc.get('file_name')
                identity = str(doc.get('_id'))
                print("type", identity)

                # Assuming file_content_binary is already in a suitable format
                image_data = f"data:image;base64,{file_content_binary}"

                socketio.emit('image_name', {
                    'content': {"data": image_data,
                                "id": identity},
                    'folder': f"{collection}"
                })




class DbReader_Ml_nude:
    MONGO_URI = 'mongodb://localhost:27017/?readPreference=primary&replicaSet=rs0'
    client = MongoClient(MONGO_URI)
    db = client["ML_Files"]

    def run(self, socketio):
        print("in run")
        self.retrive_one_doc(socketio)

    def retrive_one_doc(self, socketio):
        collections = self.db.list_collection_names()
        for collection in collections:
            if collection == "Nudity":
                coll = self.db[collection]
                doc = coll.find_one()  # Retrieve one document
                if doc:  # Ensure that a document was found
                    censored = doc.get('censored_image')
                    uncensored = doc.get('uncensored_image')
                    identity = str(doc.get('_id'))
                    image_data_c = f"data:image;base64,{censored}"
                    image_data_un = f"data:image;base64,{uncensored}"
                    print("type", identity)

                    # Assuming file_content_binary is already in a suitable format
                    # image_data = f"data:image;base64,{file_content_binary}"

                    socketio.emit('image_name', {
                                    'content': {"data": [image_data_c,image_data_un],
                                                "id": identity},
                                    'folder': f"{collection}"
                                })
                    

class Dbreader_Face:
    MONGO_URI = 'mongodb://localhost:27017/?readPreference=primary&replicaSet=rs0'
    client = MongoClient(MONGO_URI)
    db = client["Faces"]

    def run(self, socketio):
        print("in run")
        self.retrive_one_doc(socketio)

    def retrive_one_doc(self, socketio):
        collections = self.db.list_collection_names()
        for collection in collections:
            coll = self.db[collection]
            doc = coll.find_one()  # Retrieve one document
            if doc:  # Ensure that a document was found
                file_content_binary = doc.get('file_content')
                # file_name = doc.get('file_name')
                identity = str(doc.get('_id'))
                print("type", identity)

                # Assuming file_content_binary is already in a suitable format
                image_data = f"data:image;base64,{file_content_binary}"

                socketio.emit('image_name', {
                    'content': {"data": image_data,
                                "id": identity},
                    'folder': f"{collection}"
                })
