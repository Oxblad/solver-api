from unicodedata import name
from flask_sqlalchemy import SQLAlchemy
from wsgi import db
 
class Question(db.Model):

    id = db.Column(db.Integer, db.Sequence('user_id_seq'), primary_key=True)
    question = db.Column(db.String)
    answer = db.Column(db.String) 
    is_clown = db.Column(db.Integer)
    type = db.Column(db.Integer)
    floating_point = db.Column(db.Float)

class User(db.Model):
    id = db.Column(db.Integer, db.Sequence('user_id_seq'), primary_key=True)
    name = db.Column(db.String)
    

def get_questions():
    questions = Question.query.all()
    return questions 

def get_users():
    users = User.query.all()
    return users 

def add_new_question(question, answer, isClown, type=0, floating_point=0.7):  
    new_question = Question(question=question, answer=answer, is_clown=isClown, type=type, floating_point=floating_point)
    db.session.add(new_question)
    db.session.commit()

def add_new_user(user):  
    new_user = User(name=user)
    db.session.add(new_user)
    db.session.commit()
if __name__ == "__main__":

    # Run this file directly to create the database tables.
    print("Creating database tables...")
    db.create_all()
    print("DOne")