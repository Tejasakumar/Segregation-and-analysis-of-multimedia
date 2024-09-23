# from pymongo import MongoClient
# import os
# import io
# import base64
# from PIL import Image

# # Connect to MongoDB
# client = MongoClient('mongodb://localhost:27017/?readPreference=primary&replicaSet=rs0')
# db = client['Carved_Files']


# # Function to upload an image
# def upload_image(image_path, image_name):
#     with open(image_path, 'rb') as file:
#         image_data = file.read()

#     # Store the image in GridFS
#     col = db['Images']
#     document={'file_name' : image_name,
#               'file_data' : image_data
#                           }
#     col.insert_one(document)
#     print(f"Image '{image_name}' uploaded successfully.")

# def get_image():
#     col = db['Images']
    
#     docs = col.find({"file_name": "nude.jpg"})
#     for doc in docs:
#         Image.open(base64.b64decode(doc['file_data']))


# # Example usage
# upload_image('W:/Intership PES University/TASS/cory_chase.jpeg','nude.jpg')


import base64
from pymongo import MongoClient
from PIL import Image, ImageTk
import io
import os
import tkinter as tk

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['Carved_Files']
collection = db['Images']

def upload_images(folder_path):
    for filename in os.listdir(folder_path):
        
        image_path = os.path.join(folder_path, filename)
        with open(image_path, 'rb') as file:
            image_data = base64.b64encode(file.read()).decode('utf-8')

        document = {
            'file_name': filename,
            'file_data': image_data
        }
        collection.insert_one(document)
        print(f"Image '{filename}' uploaded successfully.")
def get_image(image_name):
    """
    Retrieves an image from the MongoDB database.

    Args:
        image_name (str): The name of the image to retrieve.

    Returns:
        PIL.Image or None: The retrieved image as a PIL.Image object, or None if the image is not found.
    """
    document = collection.find_one({'file_name': image_name})
    if document:
        image_data = document['file_data']
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        root = tk.Tk()

        # Convert the PIL image to a Tkinter-compatible photo image
        photo = ImageTk.PhotoImage(image)

        # Create a label to display the image
        label = tk.Label(root, image=photo)
        label.pack()

        # Start the Tkinter event loop
        root.mainloop()
        return image
    else:
        print(f"Image '{image_name}' not found.")
        return None

# Example usage
# upload_images('W:/Intership PES University/Anirudh/Images')

image = get_image('969_jpg.rf.9e5f932dd1fc8e3719f319c1af131b45.jpg')
# if image:
#     image.save('retrieved_image.jpg')
#     print("Image retrieved and saved successfully.")