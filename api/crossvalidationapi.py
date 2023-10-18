from flask import Flask, request, jsonify, send_file,Blueprint,current_app
from firebase_admin import credentials, firestore,storage
from werkzeug.utils import secure_filename
import os


##################
# db=firestore.client()

crossvalidationapi=Blueprint('crossvalidationapi',__name__)

# # # Define the upload folder
# # UPLOAD_FOLDER = 'fimages'
# ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

# # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @crossvalidationapi.route('/upload/<username>/<disease>', methods=['POST'])
# def upload_image(username, disease):
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file part'})

#     file = request.files['file']

#     if file.filename == '':
#         return jsonify({'error': 'No selected file'})

#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         # Generate a unique document ID using the username
#         document_id = username.replace(" ", "")  # Remove spaces from username
#         # Store the image URL in Firestore under the specified document ID and emotion
#         image_ref = db.collection('validation').document(document_id)
#         #image_ref.update({f'{emotion}Url': filename})
#         image_ref.set({f'{disease}Url': filename})

#         # Save the image to the upload folder
#         file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

#         return jsonify({'success': 'File uploaded successfully'})

#     return jsonify({'error': 'Invalid file type'})

# @crossvalidationapi.route('/retrieve/<username>/<disease>', methods=['GET'])
# def retrieve_image(username, disease):
#     # Generate the document ID using the username
#     document_id = username.replace(" ", "")
#     image_doc = db.collection('validation').document(document_id).get()

#     if not image_doc.exists:
#         return jsonify({'error': 'Image not found for username: ' + username}), 404

#     image_url = image_doc.to_dict().get(f'{disease}Url')
    
#     if not image_url:
#         return jsonify({'error': f'{disease} URL not found for username: ' + username}), 404
    
#     image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image_url)

#     if not os.path.exists(image_path):
#         return jsonify({'error': f'{disease} image file not found for username: ' + username}), 404
    
#     return send_file(image_path)


######

def upload_image_to_firebase(image, folder_name):
    try:
        bucket = storage.bucket()
        blob = bucket.blob(folder_name + '/' + image.filename)
        blob.upload_from_file(image)  # Use upload_from_file to upload the image
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