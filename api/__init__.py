from flask import Flask
from firebase_admin import credentials,initialize_app,storage
from flask_cors import CORS  # Import the CORS extension
import logging


cred = credentials.Certificate("C:/Users/TempO/OneDrive/Desktop/python_firebase/api/key.json")
#firebase_admin.initialize_app(cred, {'storageBucket': 'ecg-diagnosis-system'})

default_app=initialize_app(cred,{'storageBucket': 'ecg-diagnosis-system.appspot.com'})

def create_app():
    app=Flask(__name__)
    CORS(app) 
    app.config['SECRET_KEY'] = '12344gbh743'
    app.config['UPLOAD_FOLDER'] = 'resources'
    
    from .userapi import userapi
    from .modelapi import modelapi
    from .crossvalidationapi import crossvalidationapi
    
    app.register_blueprint(userapi,url_prefix='/user')
    app.register_blueprint(modelapi,url_prefix='/model')
    app.register_blueprint(crossvalidationapi,url_prefix='/crosscheck')
    
    app.logger.setLevel(logging.INFO)  # Set the desired log level
    app.logger.addHandler(logging.StreamHandler())
    return app
    
    