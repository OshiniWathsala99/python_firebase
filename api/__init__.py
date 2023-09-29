from flask import Flask
from firebase_admin import credentials,initialize_app

cred = credentials.Certificate("C:/Users/TempO/OneDrive/Desktop/python_firebase/api/key.json")
default_app=initialize_app(cred)

def create_app():
    app=Flask(__name__)
    app.config['SECRET_KEY'] = '12344gbh743'
    
    from .userapi import userapi
    from .modelapi import modelapi
    
    app.register_blueprint(userapi,url_prefix='/user')
    app.register_blueprint(modelapi,url_prefix='/model')
    return app
    
    