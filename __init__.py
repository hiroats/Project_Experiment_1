from flask import Flask
app = Flask(__name__)
import project.main  #projectの部分

#set FLASK_APP=project
#set FLASK_ENV=development
#flask run