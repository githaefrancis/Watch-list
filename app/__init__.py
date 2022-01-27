from flask import Flask
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect
from app.config import DevConfig

#Initializing the application

app=Flask(__name__,instance_relative_config=True)

app.config.from_pyfile('config.py')
app.config.from_object(DevConfig)

#Initializing flask extensions

bootstrap=Bootstrap(app)
csrf=CSRFProtect(app)

from  app import views

from app import error