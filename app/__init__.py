from flask import Flask, render_template 
from flask_bootstrap import Bootstrap5

#from flask_mail import Mail 
from flask_moment import Moment 
from flask_sqlalchemy import SQLAlchemy 
from flask_debugtoolbar import DebugToolbarExtension

from .config import config

bootstrap = Bootstrap5() 
#mail = Mail() 
moment = Moment() 
db = SQLAlchemy()
toolbar = DebugToolbarExtension()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    app.debug = True

    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    # routes
    from .main import main as main_blueprint 
    app.register_blueprint(main_blueprint)

    toolbar.init_app(app)

    return app