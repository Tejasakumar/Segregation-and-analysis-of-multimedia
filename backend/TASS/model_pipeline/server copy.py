import yaml
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import threading
from pymongo import MongoClient
from flask import *
import multiprocessing as mp
import predictionManager


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

MONGO_URI = 'mongodb://localhost:27017/'
client = AsyncIOMotorClient(MONGO_URI)
db = client["ML_Files"]

def dummy(k1,k2):
    print("k1",k1,"k2",k2)
    predictionManager.prediction(k1,k2)

@app.route('/predict', methods=['POST'])
def prediction():
    data = request.json
    print('json received')

    with open('data.yaml', 'r') as file:
        yaml_data = yaml.safe_load(file)
    true_keys = [key for key, value in data.items() if value]
    with mp.Pool(processes=len(true_keys)) as pool:
        print('enteredddddd'),
        results = [pool.apply_async(dummy, (key, yaml_data["models"][key]) ) for key in true_keys]
        for result in results:
            result.get() 

    return 'Prediction completed'


if __name__ == '__main__':
    socketio.run(app, port=8009, debug=True)