import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

class DbWriter_ML:
    __primary_string = "mongodb://localhost:27017"
    __client = AsyncIOMotorClient(__primary_string)
    __db = __client["ML_Files"]
    __path = None
    __loop = asyncio.new_event_loop()
    
    def __init__(self) -> None:
        pass
    

    def run(self, key, document,loop):
        print('came to run yolo')
        loop.run_until_complete(self.write_to_db(key,document))
        print("finished")

    async def write_to_db(self,key,doc):
        try:
            await self.__db[key].insert_one(doc)
            print("after wait data got written")
        except Exception as e:
                        print(f"Error: {e}")
    
   

    
