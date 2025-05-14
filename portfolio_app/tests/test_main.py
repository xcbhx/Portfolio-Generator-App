import unittest
from portfolio_app import create_app
from portfolio_app.extensions import db, bcrypt
from portfolio_app.models import User, Portfolio, Project

#################################################
# Global Setup Helpers
#################################################

def login(client, username, password):
  return client.post("/login", data={
      "username": username,
      "password": password
  }, follow_redirects=True)

def logout(client):
  return client.get("/logout", follow_redirects=True)

def create_user():
  password_hash = bcrypt.generate_password_hash("password").decode("utf-8")
  user = User(username="me1", password=password_hash, email="me1@example.com")
  db.session.add(user)
  db.session.commit()
  return user

def create_portfolio(user_id):
  portfolio = Portfolio(
    user_id=user_id,
    bio="Test bio for user",
    skills="Python, Flask"
  )
  db.session.add(portfolio)
  db.session.commit()
  return portfolio

def create_project(portfolio_id):
  project = Project(
    portfolio_id=portfolio_id,
    title="Sample Project",
    description="This is a test project.",
    github_link="https://github.com/example/project"
  )
  db.session.add(project)
  db.session.commit()
  return project

#################################################
# Unit Tests
#################################################

class MainTests(unittest.TestCase):

  def setUp(self):
    self.app = create_app()
    self.app.config["TESTING"] = True
    self.app.config["WTF_CSRF_ENABLED"] = False  # Disables CSRF in tests
    self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    self.client = self.app.test_client()

    with self.app.app_context():
      db.create_all()
      self.user = create_user()
      self.portfolio = create_portfolio(user_id=self.user.id)
      self.portfolio_id = self.portfolio.id   # Save ID for later use

  def tearDown(self):
    with self.app.app_context():
      db.session.remove()
      db.drop_all()

  def test_homepage_loads(self):
    response = self.client.get("/")
    self.assertEqual(response.status_code, 200)
    self.assertIn(b"Portfolio", response.data)

  def test_portfolio_detail_displays_bio(self):
    login(self.client, "me1", "password") 
    response = self.client.get(f"/portfolio/{self.portfolio.id}")
    self.assertEqual(response.status_code, 200)
    self.assertIn(self.portfolio.bio.encode(), response.data)