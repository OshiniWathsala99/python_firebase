import uuid
from flask import Blueprint,request,jsonify
from firebase_admin import firestore

db=firestore.client()
user_Ref=db.collection('user')

userapi=Blueprint('userapi',__name__)

@userapi.route('/add',methods=['POST'])
def createuser():
    try:
        id=uuid.uuid4()
        user_Ref.document(id.hex).set(request.json)
        return jsonify({"success" : True}),200
    except Exception as e:
        return f"An Error Occurs : {e}"
