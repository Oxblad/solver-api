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
 
if __name__ == "__main__":
  app.run()