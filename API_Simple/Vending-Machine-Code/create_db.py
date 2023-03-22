from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)  # Creates our app within flask
# Will wrap our app in an API and initializes the fact we're using a restful API
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:test123@localhost/Vending_Machine' #We want to config the database uri to be whatever the name of the database is and creates the database based on the current path it is in
db = SQLAlchemy() #Initialize our database with our api

class inventoryModel(db.Model):
    id = db.Column(db.Integer, primary_key = True) #Asswheigning each item in our database an id, which will be the primary key. Unique
    name = db.Column(db.String(50), nullable = False, unique = True) #nullable indicates that this field must always contain something
    quantity = db.Column(db.String(50), nullable = False)
    
with app.app_context():
    db.create_all() #Creates database. Only have to do this once unless we want to reinitialize the database