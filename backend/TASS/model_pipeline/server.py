
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from flask_socketio import SocketIO, emit
# from motor.motor_asyncio import AsyncIOMotorClient
# import asyncio
# import threading
# # from pymongo import MongoClient
# from predictionManager import PredictionManager

# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret!'
# socketio = SocketIO(app, cors_allowed_origins="*")
# CORS(app)

# MONGO_URI = 'mongodb://localhost:27017/'
# client = AsyncIOMotorClient(MONGO_URI)
# # client = MongoClient(MONGO_URI)
# db = client["ML_Files"]

# predict_manager = PredictionManager(db)

# # async def fucn(data):
# #     await asyncio.gather(predict_manager.predict(data))
# #     print('end of execution')
    
# # def func_f1(data):
# #     asyncio.run(fucn(data))

# @app.route('/predict', methods=['POST'])
# def prediction():
#     data = request.json
#     if predict_manager.check_db():
#         # Running the prediction in the main event loop
#         # loop = asyncio.new_event_loop()
#         # asyncio.set_event_loop(loop)
#         # loop.run_until_complete(predict_manager.predict(data))
#         # t1 = threading.Thread(target=predict_manager.predict,args=(data,))
#         # t1.start()
#         # t1.join()
#         predict_manager.predict(data)
#     else:
#         return "No Carved_Files detected in Databases", 404
#     return 'Prediction completed'




# if __name__ == '__main__':
#     socketio.run(app, port=8009, debug=True)
#     # app.run(port=8008,debug=True)


from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import threading
# from pymongo import MongoClient
# from predictionManager import PredictionManager
import predictionManager
import yaml
import multiprocessing as mp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

MONGO_URI = 'mongodb://localhost:27017/'
client = AsyncIOMotorClient(MONGO_URI)
# client = MongoClient(MONGO_URI)
db = client["ML_Files"]

# predict_manager = PredictionManager(db)

# def run_async_task(loop, coro):
#     asyncio.run_coroutine_threadsafe(coro, loop)

# async def func2(data):
#     await asyncio.gather(predict_manager.predict(data))

def dummy(k1,k2,val):
    print("k1",k1,"k2",k2,"val",val)
    predictionManager.prediction(k1,k2)

@app.route('/predict', methods=['POST'])
def prediction():
    data = request.json
    print('json received')
    global predict_manager
    val = predictionManager.check_db()
    print(val)
    if val!= None:
        with open('data.yaml', 'r') as file:
            yaml_data = yaml.safe_load(file)
        true_keys = [key for key, value in data.items() if value]
        with mp.Pool(processes=len(true_keys)) as pool:
            print('enteredddddd'),
            # print(pool.map(dummy, yaml_data["models"]['Cigarettes']))
            results = [pool.apply_async(dummy, (key, yaml_data["models"][key],val) ) for key in true_keys]
            for result in results:
                result.get()  # Wait for each prediction to complete
        # p1 = PredictionManager(db)
        # var = mp.Process(target=dummy)
        # var.start()
        # print(var)
        # run_async_task(loop, func2(data))
    else:
        return "No Carved_Files detected in Databases", 404
        
    return 'Prediction completed'

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on("Ready")
def segregate_images():
    socketio.start_background_task(target=run_watch)

def run_watch():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(predict_manager.some_async_function())
    loop.close()


def start_background_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    t = threading.Thread(target=start_background_loop, args=(loop,), daemon=True)
    t.start()
    socketio.run(app, port=8009, debug=True)
    # app.run(port=8008,debug=True)

