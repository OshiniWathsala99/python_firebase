from flask import Flask, request, jsonify, send_file,Blueprint,current_app
from firebase_admin import credentials, firestore,storage
from werkzeug.utils import secure_filename
import os


db=firestore.client()

crossvalidationapi=Blueprint('crossvalidationapi',__name__)

def upload_image_to_firebase(image, folder_name):
    try:
        bucket = storage.bucket()
        blob = bucket.blob(folder_name + '/' + image.filename)
        blob.upload_from_file(image) 
        return blob.public_url
    except Exception as e:
        return str(e)

@crossvalidationapi.route('/upload', methods=['POST'])
def upload_images():
    try:
        # Check if two image files are included in the request
        if 'file1' not in request.files or 'file2' not in request.files:
            return jsonify({'message': 'Two image files are required'}), 400

        image1 = request.files['file1']
        image2 = request.files['file2']

        current_app.logger.info("Attempting to upload image1")
        # Upload the images to Firebase Storage
        url1 = upload_image_to_firebase(image1, 'images')
        url2 = upload_image_to_firebase(image2, 'images')
        current_app.logger.info("Attempting send rly")
        if(url1==""):
            current_app.logger.info("null.....")
        response_data = {
            'image1_url': url1,
            'image2_url': url2,
            'success': 'File uploaded successfully'
        }

        return jsonify(response_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    
@crossvalidationapi.route('/retrive', methods=['GET'])
def get_last_properties():
  
    column_name1 = request.args.get('Date')
    column_name2 = request.args.get('user')
    
    data = db.collection('predictions').where('user', '==', column_name2).where('Date', '==', column_name1).limit(1).get()
    
    data_dict = {doc.id: doc.to_dict() for doc in data}
    return jsonify(data_dict)
