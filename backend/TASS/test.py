from pymongo import MongoClient
from bson.objectid import ObjectId
client = MongoClient('mongodb://localhost:27017/')
db = client['ML_Face_Files']
collection = db['Faces']


pipeline = [
            {"$match": {"_id": "669e2e34be51903283a78cf9"}},
            {"$project": {
                "reference_image": {"$slice": ["$reference_image", 0, 1]}
            }}
        ]
pipeline = [
            {"$match": {"_id": ObjectId('669e2e34be51903283a78cf9')}},
            {"$project": {
                "reference_image": {"$slice": [f"$reference_image", 0, 1]},
                "_id": 0  # Optionally exclude the _id field from the result
            }}
        ]
result = list(collection.aggregate(pipeline))
print(result)