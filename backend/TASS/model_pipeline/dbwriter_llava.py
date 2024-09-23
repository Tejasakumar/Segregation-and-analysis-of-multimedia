import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

class DbWriter_Llava:
    __primary_string = "mongodb://localhost:27017/?readPreference=primary&replicaSet=rs0"
    __client = AsyncIOMotorClient(__primary_string)
    __db = __client["Temp_Files"]
    __db1 = __client["ML_Files"]
    __path = None
    __loop = asyncio.new_event_loop()
    
    def __init__(self) -> None:
        pass
    
    def llava_run(self, key, doc, loop):
        #   asyncio.run(self.write_to_db(key, doc))
          loop.run_until_complete(self.write_to_db(key, doc))

    async def write_to_db(self,key, doc):
        try:
            if key not in ['Cigarettes', 'Drugs', 'Barcodes and QR codes', 'Nudity', 'Faces', 'Cars', 'Motorcycles', 'Money', 'Credit cards', 'Fire and Explosion', 'Tattoos']:
                await self.__db1[key].insert_one(doc)
                print("after wait data got written in ML_Files")
            else :
                await self.__db[key].insert_one(doc)
                print("after wait data got written in Temp_Files")
        except Exception as e:
                        print(f"Error: {e}")


    