from flask import Flask

from portfolio_app.extensions import db, login_manager, bcrypt

from portfolio_app.config import Config
from portfolio_app.models import User

from portfolio_app.main.routes import main
from portfolio_app.auth.routes import auth

import os

def create_app():
  app = Flask(__name__)
  app.config.from_object(Config)
  app.secret_key = os.urandom(24)

  # Initialize extensions
  db.init_app(app)
  login_manager.init_app(app)
  bcrypt.init_app(app)
  
  # Set login view 
  login_manager.login_view = 'auth.login'

  # User loader
  @login_manager.user_loader
  def load_user(user_id):
    return User.query.get(int(user_id))
  
  app.register_blueprint(main)
  app.register_blueprint(auth)
  
  return app