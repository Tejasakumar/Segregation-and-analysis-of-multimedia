import dbwriter1
import dbreader
import predictionManager
import dbreader_llava
import dbreader_ml
import dbwriter_ml
# import model_pipeline.dbrw_faces as dbrw_faces
import dbwriter_llava


def write_into_db():
    print("writing")
    dbw = dbwriter1.DbWriterFromLocalFolder("Output")
    dbw.run()

def forward_to_db(big_one,extensions):

    print("pushing")
    dbw = dbwriter1.PushDb(big_one,extensions)
    dbw.run()


def gettin_preview_thumb(db,socketio):
    print("fetching inital preview")
    ins1 = dbreader.DbReader()
    ins1.run(socketio)
    print("exiting preview thread")
def gettin_preview_thumb_face(db,socketio):
    print("fetching inital preview")
    ins1 = dbreader.Dbreader_Face()
    ins1.run(socketio)
    print("exiting preview thread")

def gettin_preview_thumb_ml(db,socketio):
    print("fetching inital preview")
    ins1 = dbreader.DbReader_Ml()
    ins1.run(socketio)
    print("exiting preview thread")

def gettin_preview_thumb_ml_only_nudes(db,socketio):
    print("fetching inital preview")
    ins1 = dbreader.DbReader_Ml_nude()
    ins1.run(socketio)
    print("exiting preview thread")

def dummy(k1, k2, db_data):
    print("k1",k1,"k2",k2)
    predictionManager.prediction(k1 ,k2, db_data)

def retrive_moon_docs(loop):
    return dbreader_llava.run(loop)

def write_llava_docs(key, doc,loop):
    dbl = dbwriter_llava.DbWriter_Llava()
    dbl.llava_run(key, doc, loop)

def retrive_docs(key, loop):
    return dbreader_ml.run(key, loop)

def write_docs(key, documents,loop):
    mlw = dbwriter_ml.DbWriter_ML()
    mlw.run(key, documents,loop)

def f(key, keys, db_data, val):
    print(key,'------------------',keys)
    predictionManager.prediction(key, keys, db_data)
    val.release()

def get_temp_col(loop):
    print("came to helpers for col")
    return dbreader_ml.get_cols(loop)

# def writer_faces(db, key, doc, loop):
#     w_faces = dbrw_faces.DbWriter_Faces()
#     w_faces.run_faces(db, key, doc, loop)

# def get_faces_cols(db, loop):
#     w_faces = dbrw_faces.DbWriter_Faces()
#     w_faces.get_cols(db, loop)