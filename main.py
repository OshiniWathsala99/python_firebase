# from flask import Flask, render_template, request,jsonify
# from keras.models import load_model
# from keras.preprocessing import image
# import torch
# import torch.nn as nn
# from torchvision import transforms
# from model1 import ConvNet_1
# from PIL import Image
# from torchvision import datasets
# from torch.utils.data import DataLoader

# app = Flask(__name__)

# # Load trained model weights.
# model = ConvNet_1()  
# model.load_state_dict(torch.load('C:/Users/TempO/OneDrive/Desktop/flask_api/api_fl/model_1_state_dict.pth'))

# model.eval()

# transform         = transforms.Compose(
#                                        [transforms.Resize([120,120]),
#                                         transforms.Grayscale(), 
#                                         transforms.ToTensor(),
#                                         transforms.Normalize((0.5), (0.5))
#                                        ])

# def predict_image(image_path, model, transform):
#     # Load and preprocess the image
#     image = Image.open(image_path)
#     image = transform(image).unsqueeze(0)  # Add a batch dimension

#     # Make predictions
#     with torch.no_grad():
#         outputs = model(image)
#         _, predicted = torch.max(outputs, 1)
        
#     return predicted.item()  # Return the predicted class label as an integer

# #routes
# @app.route("/", methods=["GET", "POST"])
# def main():
#     return render_template("form.html")

# @app.route("/about")
# def about():
#     return("This is about page")

# @app.route("/upload", methods=["POST"])
# def get_submitOutput():
#     if request.method=="POST":
#         img=request.files['my_image']
        
#         img_path = "C:/Users/TempO/OneDrive/Desktop/flask_api/api_fl/static" + img.filename
#         img.save(img_path)
        
#         p=predict_image(img_path, model, transform)
        
#     return jsonify({
#         'prediction' : p
#     })

# if __name__ == "__main__":
#     app.run(debug=True,port=5000)