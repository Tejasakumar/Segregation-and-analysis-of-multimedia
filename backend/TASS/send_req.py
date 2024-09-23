import requests
import json

def send_image():
    data = {
    "Flags": False,
    "Food": True,
    "Jewelry": False,
    "Maps": False,
    "Credit cards": False,
    "Money": False,
    "Faces": True,
    "Gatherings": False,
    "Hand hold object": False,
    "Nudity": True,
    "Tattoos": False,
    "Beach": False,
    "Hotel rooms": False,
    "Pool": False,
    "Restaurant": False,
    "Cigarettes": True,
    "Drugs": False,
    "Camera": False,
    "Smartphones": False,
    "Barcodes and QR codes":False,
    "Documents": False,
    "Handwriting": False,
    "Invoices": False,
    "Photo IDs": False,
    "Cars": True,
    "License plates": False,
    "Motorcycles": False,
    "Vehicle dashboards": False,
    "Fire and Explosion": False,
    "Weapons": False
    }
    

    headers = {'Content-type': 'application/json'}
    url = 'http://127.0.0.1:5000/predict'
    # files = {'file': open(image_path, 'rb')}
    response = requests.post(url,headers=headers,data=json.dumps(data))
    # print(data)

if __name__ == "__main__":
    
    prediction = send_image()
    # print(prediction)
