import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

class DbWriter_Faces:
    # __primary_string = "mongodb://localhost:27017/?readPreference=primary&replicaSet=rs0"
    # __client = AsyncIOMotorClient(__primary_string)
    # __db = __client["Faces"]

    def __init__(self) -> None:
        pass
    
    def get_cols(self, db, loop):
        loop.run_until_complete(self.face_cols(db))
    
    async def face_cols(self, db):
        try:
            return await db.list_collection_names()
        except Exception as e:
            print(f"Error in getting collections from Faces:{e}")
    
    def get_find(self,loop):
        loop.run_until_complete()
    
    # def mongo_find(se)
          

    def run_faces(self, db, key, document,loop):
        print('came to run yolo')
        loop.run_until_complete(self.write_to_db(db, key, document))
        print("finished")


    async def write_to_db(self, db, key, doc):
        try:
            await db[key].insert_one(doc)
            print("after wait data got written")
        except Exception as e:
                        print(f"Error: {e}")
    
