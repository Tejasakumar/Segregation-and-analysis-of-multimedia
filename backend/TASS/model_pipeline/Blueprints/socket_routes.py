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


socketio.on_namespace(FetchNamespace.fetchUnclassified('/raw'))
socketio.on_namespace(MLGeneralNamespace.ML_GeneralNamespace('/mlgen'))
socketio.on_namespace(MLNudeNamespace.ML_Nude_Namespace('/mlnude'))
socketio.on_namespace(MLFaceNamespace.ML_Face_Namespace('/face'))



