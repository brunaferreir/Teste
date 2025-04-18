import os
from flask import Flask
#from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['HOST'] = '0.0.0.0'
app.config['PORT']=5002
app.config['DEBUG'] = True