from flask import Flask
from flask_bootstrap import Bootstrap
# from flask_mail import Mail
# from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config,logfile


from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {
        'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default' 
        },
        'file':{
            'class': 'logging.FileHandler',
            'filename':logfile,
            'formatter':'default'
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})


bootstrap = Bootstrap()
# mail = Mail()
# moment = Moment()
db = SQLAlchemy() 

login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(config_name):
    
    app = Flask(__name__)
    app.logger.info('starting...')
    app.config.from_object(config[config_name])
    app.config['JSON_AS_ASCII'] = False

    config[config_name].init_app(app)

    bootstrap.init_app(app)
    # mail.init_app(app)
    # moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    # app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(auth_blueprint)

    return app

