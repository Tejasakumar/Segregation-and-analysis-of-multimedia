from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

MONGO_URI = 'mongodb://localhost:27017'
client = AsyncIOMotorClient(MONGO_URI)
# db = client["Carved_Files"]
db = client["Carved_Files"]
def run(loop):
        # loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop)
        # documents = loop.run_until_complete(retrieve_docs())
        # loop.close()
        # future = asyncio.Future()
        documents =  asyncio.run_coroutine_threadsafe(retrieve_docs(), loop)
    #     .add_done_callback(
    #     lambda f: future.set_result(f.result())
    # )
        # documents = future.result() 
        # documents = asyncio.run(retrieve_docs())
        return documents.result()

async def retrieve_docs():
    documents = []
    collections = await db.list_collection_names()  # Await the collection names
    for collection in collections:
        coll = db[collection]
        async for doc in coll.find({}):  # Use async for to iterate over the cursor
            file_content_binary = doc.get('file_content')
            file_name = doc.get('file_name')
            identity = str(doc.get('_id'))
            print("type", identity)
            document = {
                "file_content": file_content_binary,
                "file_name": file_name,
                "id": identity
            }
            documents.append(document)
    return documents
