from portfolio_app import db
from datetime import datetime


class User(db.Model):
  __tablename__ = "user"
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), nullable=False)
  password = db.Column(db.String(80), nullable=False)
  email = db.Column(db.String(80), nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.utcnow)

  created_portfolios = db.relationship("Portfolio", back_populates="user")

class Portfolio(db.Model):
  __tablename__ = "portfolio"
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
  bio = db.Column(db.String, nullable=False)
  skills = db.Column(db.String, nullable=False)
  projects = db.Column(db.String, nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.utcnow)

  user = db.relationship("User", back_populates="created_portfolios")
  project_list = db.relationship("Project", back_populates="portfolio")

class Project(db.Model):
  __tablename__ = "project"
  id = db.Column(db.Integer, primary_key=True)
  portfolio_id = db.Column(db.Integer, db.ForeignKey("portfolio.id"))
  title = db.Column(db.String(100), nullable=False)
  description = db.Column(db.String, nullable=False)
  github_link = db.Column(db.String, nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.utcnow)

  portfolio = db.relationship("Portfolio", back_populates="project_list")
