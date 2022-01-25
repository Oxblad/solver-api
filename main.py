import dataclasses
from flask import Flask, jsonify, request  
from config import db_link
import asyncio
from database import get_questions, add_new_question, add_new_user, get_users
import jellyfish 
from flask_sqlalchemy import SQLAlchemy
from wsgi import app

  
@app.route('/start')
async def sts(): 
    return "123"

@app.route('/solver/api/v1.0/getRespone/question=<text>', methods=['GET'])
def get_answer(text):
    questions = get_questions()  
    print(questions)
    for item in questions:
        print(item.question) 
        text = text.replace("%20", " ")
        print(f"ATr {text}")
        if item.question == text or jellyfish.jaro_distance(text, item.question) >= 0.9:    
            return jsonify({'answer': item.answer, "is_clown" : item.is_clown, "type" : item.type, "floating_point": item.floating_point}) 
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