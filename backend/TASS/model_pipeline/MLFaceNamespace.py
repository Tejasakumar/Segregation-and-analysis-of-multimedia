from motor.motor_asyncio import AsyncIOMotorClient
from flask_socketio import Namespace,emit
import threading,pymongo
import helpers 
class ML_Face_Namespace(Namespace):
    MONGO_URI = 'mongodb://localhost:27017/?readPreference=primary&replicaSet=rs0'
    client = AsyncIOMotorClient(MONGO_URI)
    db = client["Carved_Files"]
    t1 = None
    t2 = None
    FLAG = None


    def on_connect(self):
        print('raw Client connected')
        self.FLAG = True
        

    def on_disconnect(self):
        self.FLAG = False
        self.t1 = self.t2 = None
        print('raw Client disconnected from chat namespace')

    def on_Ready(self):
        print("got ready")
        if self.t1 ==  None or not (self.t1.is_alive()):
            self.t1 = threading.Thread(target=helpers.gettin_preview_thumb_face,args=(self.db,self))
            self.t1.start()
        if self.t2 == None or not self.t2.is_alive()        :
            self.t2 = threading.Thread(target=self.watcher, )
            self.t2.start()
            print("t2 started ")

    
    def watcher(self):
        secondary_string = self.MONGO_URI
        client = pymongo.MongoClient(secondary_string)
        db = client['Faces']
        existing_collections = set(db.list_collection_names())


        while self.FLAG:
            current_collections = set(db.list_collection_names())
            new_collections = current_collections - existing_collections
            if new_collections:
                print(new_collections)
                for collection in new_collections:
                    client1 = pymongo.MongoClient(secondary_string)
                    db1 = client1['Faces']
                    coll = db1[collection]
                    print(f"Checking collection: {collection}")
                    print(f"Document count: {coll.count_documents({})}")
                    doc_count = coll.count_documents({})
                    if doc_count > 0:
                        for doc in coll.find().limit(1):
                            file_content_binary = doc.get('file_content')
                            identity = str(doc.get('_id'))
                            image_data = f"data:image;base64,{file_content_binary}"
                            print(identity)
                            super().emit('image_name', {
                                'content': {"data": image_data,
                                            "id": identity},
                                'folder': f"{collection}"
                            })
                        existing_collections = current_collections