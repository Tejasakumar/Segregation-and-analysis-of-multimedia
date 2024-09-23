from flask import request,Flask,jsonify, make_response
from flask_cors import *
from flask_socketio import * 
import E01Processor
import BinProcessor
import helpers
import multiprocessing
from Blueprints import socketio,socketio_blueprint
import pymongo
from bson import json_util
import yaml
import asyncio, threading
import requests
from detect_face import Face_match
import json


app = Flask(__name__)
CORS(app)
socketio.init_app(app, cors_allowed_origins="*", async_mode='threading')
app.register_blueprint(socketio_blueprint)
MONGO_URI = 'mongodb://localhost:27017/?readPreference=primary&replicaSet=rs0'



@app.route("/dump", methods=["GET", "POST"])
def receive_dump():
    if request.method == "POST":
        data = request.get_json()
        print(list(data["result"].keys()))
        data = data["result"]
        # data = {
        # extractor = Scalpel
        # files_array = [{name,content,extension},{name,content,extension}]
        # }
        if len(data):
            array = data["files_array"]  # type is a list
            print(data["extractor"])
            analyzer = None
            extension = array[0]["extension"]
            if extension == "E01":
                analyzer = E01Processor.E01Processor(array, data["extractor"])
            else:
                analyzer = BinProcessor.BinProcessor(array, data["extractor"])
            print("suksuks")
            analyzer.setupDump()
            analyzer.startAnalysis()
            # run_async_task_gpt(loop, func2())
            process = multiprocessing.Process(target=helpers.write_into_db)
            process.start()

        return jsonify({'status': 'File processed'}), 200
    return "not Handled request", 400

@app.route("/photos",methods=["POST"])
def put_photos_to_db():
    req = request.get_json()
    jpeg_document = []
    jpg_document = []
    png_document = []
    tiff_document = []
    big_one = [jpeg_document, jpg_document, png_document, tiff_document]
    extensions = ["jpeg", "jpg", "png", "tiff"]
    
    for i in req["result"]:
        collection_name = i["name"]
        extension = collection_name.split(".")[-1]
        
        doc = {
            "file_name": i["name"],
            "file_content": i["content"]
        }

        if extension == "jpg":
            jpg_document.append(doc)
        elif extension == "png":
            png_document.append(doc)
        elif extension == "jpeg":
            jpeg_document.append(doc)
        elif extension == "tiff":
            tiff_document.append(doc)

    process = multiprocessing.Process(target=helpers.forward_to_db, args=(big_one,extensions))
    process.start()
    
    return jsonify({'status': 'photos uploaded'}), 200

@app.route("/fetchphotos", methods=["GET"])
def get_photos():
    cli = pymongo.MongoClient(MONGO_URI)
    db = str(request.args.get("db"))
    print(db)
    if db == "Mlgen":
        db = cli["ML_Files"]
    elif db =="carved":
        db = cli['Carved_Files']
    elif db == "faces":
        db = cli["Faces"]
    num_of_photos = int(request.args.get('count'))
    size = int(request.args.get('size', 18))
    coll = str(request.args.get("coll"))
    
    print("database"+str(db)+"numberof_photos"+str(num_of_photos)+" collection "+str(coll))
    collection = db[coll]
    photos = list(collection.find().skip(num_of_photos).limit(size))
    res = {
        "photos": photos
    }
    cli.close()
    return json_util.dumps(res)



@app.route('/predict', methods=['POST'])
def prediction():
    val = multiprocessing.Lock()
    data = request.json
    print('json received')
    with open('data.yaml', 'r') as file:
        yaml_data = yaml.safe_load(file)
    true_keys = [key for key, value in data.items() if value]  #later change true_keys to keys while doing cookies
    

    """true_keys = []
    old_keys = json.loads(request.cookies.get('activated_models',""))
    if old_keys=="":
        true_keys=keys
    else:
        true_keys = [item for item in keys not in old_keys]
    cookie_resp = json.dumps(true_keys + old_keys)
    resp = make_response("Setting cookies")
    resp.set_cookie('activated_models', cookie_resp)"""


    if len(true_keys)>0:

        print("in ifffff")
        db_data = helpers.retrive_moon_docs(loop)
        pm = multiprocessing.Process(target=helpers.f, args=('Llava', true_keys, db_data, val))
 
        val.acquire()
        pm.start()
        pm.join()

        while True:
            if val.acquire(block=False):
                val.release()   
                break
        
        print("olllavaaa doneeeeeeeeeeeeeeeeeeeee")
        col_names = helpers.get_temp_col(loop)
        print(col_names)
        print("printtttttttttttttttttt")
        with multiprocessing.Pool(processes=len(col_names)) as pool:
            print('enteredddddd')
            # results = [pool.apply_async(helpers.dummy, (key, yaml_data["models"][key], db_data) ) for key in true_keys]
            results = []
            for key in col_names:
                temp_data = helpers.retrive_docs(key, loop)
                p = multiprocessing.Process(target=helpers.dummy, args=(key, yaml_data['models'][key], temp_data))
                results.append(p)
                p.start()
            for result in results:
                result.join()

        return 'Prediction completed'
    else: return "The User did not ask for AI Prediction"


@app.route("/faces")
def faces():
    return "at face",200

@app.route("/test",methods=["POST"])
def testof():
    data = request.json
    fm = Face_match()
    print(fm.match(data['fileContents']))
    return fm.match(data['fileContents'])


@app.route("/file-summary", methods=['POST'])
def filesummary():
    text=""
    data = request.json
    image = data['file']
    prompt = data['prompt']
    with open('data.yaml', 'r') as file:
        yaml_data = yaml.safe_load(file)
    port = yaml_data['ollama']['port']
    url = f"http://127.0.0.1:{port}/api/generate"
    data = {
        "model": "investigator",
        "prompt": prompt,
        "images": [image],
        "stream": False
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        text = response.json().get('response')
        print(text)
    return text,200     

def start_background_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    t = threading.Thread(target=start_background_loop, args=(loop,), daemon=True)
    t.start()
    socketio.run(app,debug=True)