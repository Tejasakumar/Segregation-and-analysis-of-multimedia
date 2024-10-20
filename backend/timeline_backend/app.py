import os
import base64
import pymongo
from flask import Flask, jsonify, send_file, request
from PIL import Image, ExifTags
from datetime import datetime
import subprocess
from flask_cors import CORS
from py_mini_racer import MiniRacer
from io import BytesIO

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

MONGO_URI = 'mongodb://localhost:27017/'
client = pymongo.MongoClient(MONGO_URI)
db = client["image_database"]
collection_with_data = db["images_with_data"]
collection_without_data = db["images_without_data"]

js_code = """
function convertDMSToDD(dmsArray, direction) {
    if (!Array.isArray(dmsArray) || dmsArray.length !== 3) {
      return null;
    }
    
    const [degrees, minutes, seconds] = dmsArray;
    let dd = degrees + minutes / 60 + seconds / 3600;
    
    if (direction === 'S' || direction === 'W') {
      dd = dd * -1;
    }
    
    return parseFloat(dd.toFixed(6));
}

function parseExifDate(dateString) {
    if (!dateString) return null;
    
    const [datePart, timePart] = dateString.split(' ');
    const [year, month, day] = datePart.split(':');
    const [hour, minute, second] = timePart ? timePart.split(':') : [0, 0, 0];
    
    return new Date(year, month - 1, day, hour, minute, second).toISOString();
}

function processImageData(file, stats, exifData) {
    let latitude = null;
    let longitude = null;
    let timestamp = new Date(stats.mtime).toISOString();

    if (exifData && exifData.GPSInfo) {
        const latitudeRef = exifData.GPSInfo.GPSLatitudeRef;
        const longitudeRef = exifData.GPSInfo.GPSLongitudeRef;
        const latitudeArray = exifData.GPSInfo.GPSLatitude ? exifData.GPSInfo.GPSLatitude.slice(1, -1).split(',').map(Number) : null;
        const longitudeArray = exifData.GPSInfo.GPSLongitude ? exifData.GPSInfo.GPSLongitude.slice(1, -1).split(',').map(Number) : null;

        if (latitudeArray && longitudeArray) {
            latitude = convertDMSToDD(latitudeArray, latitudeRef);
            longitude = convertDMSToDD(longitudeArray, longitudeRef);
        }
    }

    if (exifData && exifData.DateTimeOriginal) {
        const parsedDate = parseExifDate(exifData.DateTimeOriginal);
        if (parsedDate) {
            timestamp = parsedDate;
        }
    }

    return { 
        fileName: file, 
        latitude, 
        longitude, 
        timestamp,
        thumbnailUrl: `/thumbnails/${file}`
    };
}
"""

ctx = MiniRacer()
ctx.eval(js_code)

def get_exif_data_from_bytes(image_bytes):
    try:
        image = Image.open(BytesIO(image_bytes))
        exif_data = image._getexif()
        if exif_data is None:
            return None
        
        converted_exif = {}
        for tag_id, value in exif_data.items():
            tag = ExifTags.TAGS.get(tag_id, tag_id)
            if tag == 'GPSInfo':
                gps_data = {}
                for t in value:
                    gps_tag = ExifTags.GPSTAGS.get(t, t)
                    gps_data[gps_tag] = str(value[t])
                converted_exif[tag] = gps_data
            elif isinstance(value, bytes):
                converted_exif[tag] = value.decode('utf-8', errors='replace')
            elif isinstance(value, (int, float, str)):
                converted_exif[tag] = value
            else:
                converted_exif[tag] = str(value)
        return converted_exif
    except Exception as e:
        print(f"Error extracting EXIF data: {e}")
        return None

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/thumbnails/<path:filename>')
def thumbnails(filename):
    try:
        image_data = collection_with_data.find_one({"file_name": filename})
        if image_data is None:
            image_data = collection_without_data.find_one({"file_name": filename})
        if image_data is None:
            return jsonify(error="Image not found"), 404
        image_bytes = base64.b64decode(image_data["file_content"])
        image_io = BytesIO(image_bytes)
        return send_file(image_io, mimetype='image', as_attachment=False, download_name=filename)
    except Exception as e:
        print(f"Error retrieving thumbnail: {str(e)}")
        return jsonify(error='Failed to fetch thumbnail'), 500

@app.route('/api/images', methods=['GET'])
def get_images():
    try:
        images = list(collection_with_data.find({}))
        image_data = []
        for file in images:
            try:
                image_id = file["_id"]
                image_name = file["file_name"]
                stats = datetime.now().timestamp()
                image_bytes = base64.b64decode(file["file_content"])
                exif_data = get_exif_data_from_bytes(image_bytes)
                #print(f"EXIF data for {file}:", exif_data)
                result = ctx.call('processImageData', image_name, {'mtime': stats * 1000}, exif_data)
                #print(f"Processed data for {file}:", result)
                image_data.append(result)
            except Exception as e:
                print(f"Error processing file {file}: {str(e)}")
        
        filtered_image_data = [img for img in image_data if img['latitude'] is not None and img['longitude'] is not None]
        #print(f"Total images: {len(image_data)}, Images with GPS data: {len(filtered_image_data)}")
        return jsonify(filtered_image_data)
    
    except Exception as e:
        #print(f"Error reading images directory: {str(e)}")
        return jsonify(error='Failed to fetch image data'), 500
@app.route('/api/images-without-metadata', methods=['GET'])
def get_images_without_metadata():
    try:
        images = list(collection_without_data.find({}, {'_id': 0, 'file_name': 1, 'exif_data': 1}))
        image_metadata = []
        for img in images:
            exif_data = img.get('exif_data', None)
            if exif_data is None or not exif_data:
                message = "No EXIF data available"
                image_metadata.append({
                    'filename': img['file_name'],
                    'imageUrl': f'http://127.0.0.1:4000/thumbnails/{img["file_name"]}',
                    'metadata': {
                        'message': message
                    }
                })
            else:
                dimensions = f"{exif_data.get('ExifImageWidth', 'Unknown')}x{exif_data.get('ExifImageHeight', 'Unknown')}"
                timestamp = exif_data.get('timestamp', 'Unknown')
                gps_info = exif_data.get('GPSInfo', 'Unknown')
                image_metadata.append({
                    'filename': img['file_name'],
                    'imageUrl': f'http://127.0.0.1:4000/thumbnails/{img["file_name"]}',
                    'metadata': {
                        'DateTimeOriginal': timestamp,
                        'GPSInfo': gps_info,
                        'ExposureTime': exif_data.get('ExposureTime', 'Unknown'),
                        'FNumber': exif_data.get('FNumber', 'Unknown'),
                        'ISO': exif_data.get('ISOSpeedRatings', 'Unknown'),
                        'dimensions': dimensions,
                        'Make': exif_data.get('Make', 'Unknown'),
                        'Model': exif_data.get('Model', 'Unknown'),
                        'hasDateTime': 'DateTime' in exif_data,
                        'hasLocation': 'GPSInfo' in exif_data
                    }
                })
        
        return jsonify({'images': image_metadata})
    except Exception as e:
        print(f"Error retrieving images without metadata: {str(e)}")
        return jsonify(error='Internal server error'), 500
    
@app.route('/api/get-image-dates', methods=['POST'])
def get_image_dates():
    try:
        data = request.get_json()
        page = data.get('page', 1)
        size = data.get('size', 2)
        skip = (page - 1) * size
        images = collection_with_data.find().skip(skip).limit(size)
        image_data = []

        for image in images:
            try:
                image_id = image["_id"]
                image_bytes = base64.b64decode(image["file_content"])
                image_name = image["file_name"]  
                exif_data = get_exif_data_from_bytes(image_bytes)
                fake_mtime = datetime.now().timestamp()
                result = ctx.call('processImageData', image_name, {'mtime': fake_mtime * 1000}, exif_data)
                image_data.append(result)
            except Exception as e:
                print(f"Error processing image {image_id}: {str(e)}")
        image_data.sort(key=lambda x: x['timestamp'])
        print(f"Processed image data: {image_data}")
        return jsonify(image_data)
    except Exception as e:
        print(f"Error processing images: {str(e)}")
        return jsonify(error='Failed to process images'), 500

if __name__ == '__main__':
    # subprocess.Popen(['python', 'upload_to_mongodb.py', './pics'])
    app.run(debug=True, port=4000)
