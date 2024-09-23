from motor.motor_asyncio import AsyncIOMotorClient
import asyncio



MONGO_URI = 'mongodb://localhost:27017/?readPreference=primary&replicaSet=rs0'
client = AsyncIOMotorClient(MONGO_URI)
# db = client["Carved_Files"]
db = client["Temp_Files"]

def get_cols(loop):
    print("db.list_collection_names()")
    cols = asyncio.run_coroutine_threadsafe(retrieve_cols(), loop) 
    print(cols)
    return cols.result()

async def retrieve_cols():
    return await db.list_collection_names()

def run(key, loop):
        # loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop)
        # documents = loop.run_until_complete(retrieve_docs())
        # loop.close()
        # future = asyncio.Future()
        documents =  asyncio.run_coroutine_threadsafe(retrieve_docs(key), loop)
    #     .add_done_callback(
    #     lambda f: future.set_result(f.result())
    # )
        # documents = future.result() 
        # documents = asyncio.run(retrieve_docs())
        print('chutttt',type(documents))
        return documents.result()

async def retrieve_docs(key):
    documents = []
    coll = db[key]
    async for doc in coll.find({}):  # Use async for to iterate over the cursor
        documents.append(doc)
    return documents
