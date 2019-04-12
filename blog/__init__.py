from flask import Flask 
from flask_sqlalchemy import SQLAlchemy

from config import Config

app = Flask(__name__)

app.config.from_object('config')

db = SQLAlchemy(app)


from blog.admin.controllers import admin_mod 
from blog.site.controllers import site_mod 

app.register_blueprint(admin_mod)
app.register_blueprint(site_mod)

db.create_all()