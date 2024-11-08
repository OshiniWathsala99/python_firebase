from flask import Flask, request, jsonify, send_file,Blueprint,current_app
from firebase_admin import credentials, firestore
from werkzeug.utils import secure_filename
import os

db=firestore.client()

crossvalidationapi=Blueprint('crossvalidationapi',__name__)

# # Define the upload folder
# UPLOAD_FOLDER = 'fimages'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@crossvalidationapi.route('/upload/<username>/<disease>', methods=['POST'])
def upload_image(username, disease):
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Generate a unique document ID using the username
        document_id = username.replace(" ", "")  # Remove spaces from username
        # Store the image URL in Firestore under the specified document ID and emotion
        image_ref = db.collection('validation').document(document_id)
        #image_ref.update({f'{emotion}Url': filename})
        image_ref.set({f'{disease}Url': filename})

        # Save the image to the upload folder
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        return jsonify({'success': 'File uploaded successfully'})

    return jsonify({'error': 'Invalid file type'})

@crossvalidationapi.route('/retrieve/<username>/<disease>', methods=['GET'])
def retrieve_image(username, disease):
    # Generate the document ID using the username
    document_id = username.replace(" ", "")
    image_doc = db.collection('validation').document(document_id).get()

    if not image_doc.exists:
        return jsonify({'error': 'Image not found for username: ' + username}), 404

    image_url = image_doc.to_dict().get(f'{disease}Url')
    
    if not image_url:
        return jsonify({'error': f'{disease} URL not found for username: ' + username}), 404
    
    image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image_url)

    if not os.path.exists(image_path):
        return jsonify({'error': f'{disease} image file not found for username: ' + username}), 404
    
    return send_file(image_path)
