import time
import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from bson.binary import Binary
import base64

class DbWriterFromLocalFolder:
    __primary_string = "mongodb://localhost:27017/?readPreference=primary&replicaSet=rs0"
    __client = AsyncIOMotorClient(__primary_string)
    __db = __client["Carved_Files"]
    # __db = __client["tejas_carved_files"]
    __path = None
    __loop = asyncio.new_event_loop()
    
    def __init__(self,path) -> None:
        self.__path = path 
        # asyncio.set_event_loop(self.__loop)
        
    def run(self):
        # self.__loop.run_until_complete(self.get_dirs(self.__path))
        asyncio.run(self.get_dirs(self.__path))

    async def write_to_db(self,path,collection):
        try:
            with open(path, 'rb') as f:
                await self.__db[collection].insert_one({
                    "file_content": base64.b64encode(f.read()).decode('utf-8'),
                    "file_name": path.split("\\")[-1]
                })
        except Exception as e:
                        print(f"Could not read file {path}: {e}")


    async def read_files(self,start_directory):
        print('sdfghjk')
        for root, dirs, files in os.walk(start_directory):
            # print(root.split("\\")[-1])
            col = root.split("\\")[-1]
            tasks = []
            if  col != "Output":
                print("root = ", root)
                for file in files:
                    file_path = os.path.join(root, file)
                    tasks.append(self.write_to_db(file_path, col))
                await asyncio.gather(*tasks)
            else:
                continue


    async def get_dirs(self,start_dir):
        start_dir = os.path.abspath(start_dir)

        print("in getdirs",start_dir)
        tasks = []
        print(start_dir)
        for root,dirs,files in os.walk(start_dir):
            print(dirs)
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                tasks.append(self.read_files(dir_path))
        print(tasks)
        await asyncio.gather(*tasks)
    


    # # Example usage:
    # start = time.time()
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    # loop.run_until_complete(get_dirs(start_directory))
    # print("time taken for execution = ", time.time()-start)
# start_directory = 'Playground\Output'
# DbWriter(start_directory).run()

class PushDb:
    MONGO_URI = 'mongodb://localhost:27017/?readPreference=primary&replicaSet=rs0'
    client = AsyncIOMotorClient(MONGO_URI)
    db = client["Carved_Files"]
    big_one = None
    extensions=None
    def __init__(self,big_one,extensions):
        self.big_one = big_one
        self.extensions = extensions

    async def insert(self,extension, data):
        collection = self.db[extension]
        result = await collection.insert_many(data)

    async def insert_all(self):
        tasks = []
        for k in range(len(self.big_one)):
            if len(self.big_one[k]):
                tasks.append(self.insert(self.extensions[k],self.big_one[k]))
        await asyncio.gather(*tasks)
    
    def run(self):
        asyncio.run(self.insert_all())
