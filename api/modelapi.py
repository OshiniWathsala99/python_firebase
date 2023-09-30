import uuid
from flask import Blueprint,request,jsonify,Flask
from firebase_admin import firestore
from keras.models import load_model
from keras.preprocessing import image
import torch
import torch.nn as nn
from torchvision import transforms
from api.model1 import ConvNet_1
from PIL import Image
from torchvision import datasets
from torch.utils.data import DataLoader

db=firestore.client()
user_Ref=db.collection('predictions')

modelapi=Blueprint('modelapi',__name__)

# Load trained model weights.
model = ConvNet_1()  
model.load_state_dict(torch.load('C:/Users/TempO/OneDrive/Desktop/python_firebase/api/model_1_state_dict.pth'))

model.eval()

transform         = transforms.Compose(
                                       [transforms.Resize([120,120]),
                                        transforms.Grayscale(), 
                                        transforms.ToTensor(),
                                        transforms.Normalize((0.5), (0.5))
                                       ])

def predict_image(image_path, model, transform):
    # Load and preprocess the image
    image = Image.open(image_path)
    image = transform(image).unsqueeze(0)  # Add a batch dimension

    # Make predictions
    with torch.no_grad():
        outputs = model(image)
        _, predicted = torch.max(outputs, 1)
        
    return predicted.item()  # Return the predicted class label as an integer

@modelapi.route('/save',methods=['POST'])
def createrecord():
    try:
        id=uuid.uuid4()
        user_Ref.document(id.hex).set(request.json)
        return jsonify({"success" : True}),200
    except Exception as e:
        return f"An Error Occurs : {e}"
    
    
@modelapi.route('/previous',methods=['GET'])
def retriverecords():
    column_name = request.args.get('name')

    # Replace 'your_collection' with the name of your Firestore collection
    # This query filters documents where 'column_name' equals a specific value
    data = db.collection('predictions').where('user', '==', column_name).get()
    
    data_dict = {doc.id: doc.to_dict() for doc in data}
    return jsonify(data_dict)
    

@modelapi.route("/upload", methods=["POST"])
def get_submitOutput():
    if request.method=="POST":
        img=request.files['my_image']
        
        img_path = "C:/Users/TempO/OneDrive/Desktop/flask_api/api_fl/static" + img.filename
        img.save(img_path)
        
        p=predict_image(img_path, model, transform)
        
    return jsonify({
        'prediction' : p      
})