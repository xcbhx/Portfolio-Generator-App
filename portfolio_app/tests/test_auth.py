import unittest
from portfolio_app import create_app
from portfolio_app.extensions import db, bcrypt
from portfolio_app.models import User

#################################################
# Global Setup Helper
#################################################

def create_user():
  password_hash = bcrypt.generate_password_hash("password").decode("utf-8")
  user = User(username="me1", email="me1@example.com", password=password_hash)
  db.session.add(user)
  db.session.commit()
  return user

#################################################
# Unit Tests
#################################################

class AuthTests(unittest.TestCase):

  def setUp(self):
    self.app = create_app()
    self.app.config["TESTING"] = True
    self.app.config["WTF_CSRF_ENABLED"] = False
    self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    self.client = self.app.test_client()

    with self.app.app_context():
      db.create_all()
      create_user()

  def tearDown(self):
    with self.app.app_context():
      db.session.remove()
      db.drop_all()

  def test_login_success(self):
    response = self.client.post("/login", data={
        "username": "me1",
        "password": "password"
    }, follow_redirects=True)
    self.assertEqual(response.status_code, 200)
    self.assertIn(b"Portfolio", response.data)

  def test_login_failure(self):
    response = self.client.post("/login", data={
        "username": "me1",
        "password": "wrongpassword"
    }, follow_redirects=True)
    self.assertEqual(response.status_code, 200)
    self.assertIn(b"Incorrect username or password.", response.data)

  def test_logout(self):
    self.client.post("/login", data={
        "username": "me1",
        "password": "password"
    }, follow_redirects=True)

    response = self.client.get("/logout", follow_redirects=True)
    self.assertEqual(response.status_code, 200)
    self.assertIn(b"Login", response.data)
  
  def test_signup_success(self):
    response = self.client.post("/signup", data={
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "newpassword"
    }, follow_redirects=True)
    self.assertEqual(response.status_code, 200)
    self.assertIn(b"Account Created.", response.data) 

    # Optionally check that the user was created in the database
    with self.app.app_context():
      user = User.query.filter_by(username="newuser").first()
      self.assertIsNotNone(user)
    print(response.data.decode())

