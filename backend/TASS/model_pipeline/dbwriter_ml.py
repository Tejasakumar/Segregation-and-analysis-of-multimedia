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
        # # asyncio.set_event_loop(loop)
        # # asyncio.run_coroutine_threadsafe(self.write_to_db(key, document))
        # # asyncio.create_task(self.yolo_write(key, doc))
        # self.write_to_db(key,document)
        loop.run_until_complete(self.write_to_db(key,document))
        print("finished")

   

    async def write_to_db(self,key,doc):
        try:
            await self.__db[key].insert_one(doc)
            print("after wait data got written")
        except Exception as e:
                        print(f"Error: {e}")
    
    # async def db_moon_write(self, all_docs):
    #     tasks = []
    #     for docs in all_docs:
    #         for col, doc in docs:
    #             tasks.append(self.write_to_db(col, doc))
    #     await asyncio.gather(*tasks)

    # async def db_write(self, key, documents):
    #     print("eb_write")
    #     tasks = []
    #     for doc in documents:
    #         print(doc)
    #         tasks.append(self.write_to_db(key, doc))
    #     await asyncio.gather(*tasks)

        # await self.__db[key].insert_one(doc)
        # return f"{doc['file_name']} stored"
        # asyncio.run(self.get_dirs(self.__path, collection))

    


    # async def read_files(self,start_directory):
    #     print('sdfghjk')
    #     for root, dirs, files in os.walk(start_directory):
    #         # print(root.split("\\")[-1])
    #         col = root.split("\\")[-1]
    #         tasks = []
    #         if  col != "Output":
    #             print("root = ", root)
    #             for file in files:
    #                 file_path = os.path.join(root, file)
    #                 tasks.append(self.write_to_db(file_path, col))
    #             await asyncio.gather(*tasks)
    #         else:
    #             continue


    # async def get_dirs(self,start_dir):
    #     start_dir = os.path.abspath(start_dir)

    #     print("in getdirs",start_dir)
    #     tasks = []
    #     print(start_dir)
    #     for root,dirs,files in os.walk(start_dir):
    #         print(dirs)
    #         for dir in dirs:
    #             dir_path = os.path.join(root, dir)
    #             tasks.append(self.read_files(dir_path))
    #     print(tasks)
    #     await asyncio.gather(*tasks)

    