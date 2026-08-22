from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = \
    "mysql+pymysql://root:Mysql@2023@localhost/school"

db.init_app(app)