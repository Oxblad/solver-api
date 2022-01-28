import dataclasses
from flask import Flask, jsonify, request  
from config import db_link
import asyncio
from database import get_questions, add_new_question, add_new_user, get_users
import jellyfish 
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import db_link
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
app = Flask(__name__)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["1 minute"]
)
# Set up the SQLAlchemy Database to be a local file 'desserts.db'
app.config['SQLALCHEMY_DATABASE_URI'] = db_link
app.config['JSON_AS_ASCII'] = False 
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["postgresqlPostgresConnectionLimit"] = 200
db = SQLAlchemy(app)
db.create_all()
 
 
 
  
@app.route('/start')
def sts(): 
    return "123"

@app.route('/solver/api/v1.0/getRespone/', methods=['GET'])
@limiter.limit("3 minute")
def get_answer():
    questions = get_questions()  
    data = []
    for item in questions:
        data.append({"question" : item.question, "answer" : item.answer, "is_clown" : item.is_clown, "type": item.type, "floating_point" : item.floating_point})
    return jsonify(data)  
@app.route('/solver/api/v1.0/addQuestion/', methods=['POST'])
@limiter.limit("3 minute")
def create_task(): 
    if not request.json: 
        return jsonify({'result': False})
    question = request.json['question']
    answer = request.json.get('answer', "")
    is_clown = int(request.json.get('is_clown', ""))
    type = int(request.json.get('type', ""))
    floating_point = float(request.json.get('floating_point', ""))
    add_new_question(question, answer, is_clown, type, floating_point)
 
    return jsonify({'result': True}), 201

@app.route('/user/api/v1.0/check/user=<text>', methods=['GET'])
@limiter.limit("3 minute")
def get_lzt_user(text):
    users = get_users()  
    for item in users:
        if item.name == text:    
            return "Yes"
    return "No"

@app.route('/users/api/v1.0/addUser/', methods=['POST'])
@limiter.limit("3 minute")
def add_lzt_user(): 
    print("ALLLASDFLLFLFD")
    if not request.json: 
        return jsonify({'result': False})
    user = request.json['user'] 
    add_new_user(user)
 
    return jsonify({'result': True}), 201

if __name__ == "__main__":
  app.run()
