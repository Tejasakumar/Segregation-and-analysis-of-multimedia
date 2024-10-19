from header_files.predict_headers import *


def prediction(key, model_path, db_data):
    
    if key == 'Cigarettes':
        print('cigs')
        # print(db_carved, key, db)
        predict_instance = Predict_Cigarettes(model_path) 
        predict_instance.predict(key, db_data)

    elif key == 'Drugs':
        print('drugs')
        predict_instance = Predict_Drugs(model_path)
        predict_instance.predict(key, db_data)

    elif key == 'Barcodes and QR codes':
        print('qr')
        predict_instance = Predict_QR(model_path)
        predict_instance.predict(key, db_data)
    
    elif key == 'Nudity':
        print('Nudity')
        predict_instance = Predict_Nudity()
        predict_instance.predict(key, db_data)

    elif key == 'Faces':
        print('Faces')
        predict_instance = Predict_LightFace()
        predict_instance.predict(key, db_data)
        
    elif key == 'Cars':
        print('Cars')
        predict_instance = Predict_Cars(model_path)
        predict_instance.predict(key, db_data)

    elif key == 'Motorcycles':
        print('Motorcycles')
        predict_instance = Predict_Motorcycles(model_path)
        predict_instance.predict(key, db_data)

    elif key == 'Money':
        print('Money')
        predict_instance = Predict_Money(model_path)
        predict_instance.predict(key, db_data)

    elif key == 'Credit cards':
        print('Credit cards')
        predict_instance = Predict_Credit(model_path)
        predict_instance.predict(key, db_data)

    elif key == 'Fire and Explosion':
        print('Fire and Explosion')
        predict_instance = Predict_Fire(model_path)
        predict_instance.predict(key, db_data)
    
    elif key == 'Tattoos':
        print('Tattoos')
        predict_instance = Predict_Tattoos(model_path)
        predict_instance.predict(key, db_data)
    
    elif key == "Llava":
        print('llavaaa')
        predict_instance = Predict_Llava()
        predict_instance.predict(model_path, db_data)
        
