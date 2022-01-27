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

app = Flask(__name__)

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

@app.route('/solver/api/v1.0/getRespone/question=<text>', methods=['GET'])
def get_answer(text):
    questions = get_questions()  
    print(f"question: {text}")
    for item in questions: 
        text = text.replace("%20", " ")
        print(item.question) 
        print(item.question == text) 
        print(jellyfish.jaro_distance(text, item.question))
        item.question = item.question.replace("?", "")
        if item.question == text or jellyfish.jaro_distance(text, item.question) >= item.floating_point:    
            return jsonify({'answer': item.answer, "is_clown" : item.is_clown, "type" : item.type, "floating_point": item.floating_point}) 
        print("----")
    return "No"

@app.route('/solver/api/v1.0/addQuestion/', methods=['POST'])
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
def get_lzt_user(text):
    users = get_users()  
    for item in users:
        if item.name == text:    
            return "Yes"
    return "No"

@app.route('/users/api/v1.0/addUser/', methods=['POST'])
def add_lzt_user(): 
    print("ALLLASDFLLFLFD")
    if not request.json: 
        return jsonify({'result': False})
    user = request.json['user'] 
    add_new_user(user)
 
    return jsonify({'result': True}), 201

if __name__ == "__main__":
  app.run()
