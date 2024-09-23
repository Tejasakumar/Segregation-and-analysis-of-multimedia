# your_blueprint/socket_routes.py
from flask import Blueprint
from flask_socketio import SocketIO, emit
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import threading
import helpers
import FetchNamespace 
import MLGeneralNamespace
import MLNudeNamespace
import MLFaceNamespace


socketio_blueprint = Blueprint('socketio_blueprint', __name__)
socketio  = SocketIO(cross_origin="*", async_mode='threading')
t1 = None

# MONGO_URI = 'mongodb://localhost:27017/?readPreference=primary&replicaSet=rs0'
# client = AsyncIOMotorClient(MONGO_URI)
# db = client["tejas_carved_files"]

# @socketio.on('connect',namespace="/raw")
# def handle_connect():
#     print('Client connected')


# @socketio.on('connect', namespace="/ml")
# def handle_connect():
#     print('ML Client connected')
    

# @socketio.on('disconnect')
# def handle_disconnect():
#     print('Client disconnected')

# @socketio.on('Ready')
# def handle_message():
#     print("got ready")
#     t1 = threading.Thread(target=helpers.gettin_preview_thumb,args=(db,socketio))
#     t1.start()

socketio.on_namespace(FetchNamespace.fetchUnclassified('/raw'))
socketio.on_namespace(MLGeneralNamespace.ML_GeneralNamespace('/mlgen'))
socketio.on_namespace(MLNudeNamespace.ML_Nude_Namespace('/mlnude'))
socketio.on_namespace(MLFaceNamespace.ML_Face_Namespace('/face'))



