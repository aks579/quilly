from flask import Flask
from app import config

app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['DEBUG'] = config.DEBUG
app.config['FOLDER'] = config.FOLDER
app.config['ATTACHMENTS'] = config.ATTACHMENTS

from app import routes
from app import tags
tags.load_tags_data()
