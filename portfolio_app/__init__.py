from flask import Flask
from portfolio_app.config import Config
from portfolio_app.extensions import db
import os

def create_app():
  app = Flask(__name__)
  app.config.from_object(Config)
  app.secret_key = os.urandom(24)

  db.init_app(app)
  
  from portfolio_app.routes import main
  app.register_blueprint(main)

  with app.app_context():
    db.create_all()
  
  return app