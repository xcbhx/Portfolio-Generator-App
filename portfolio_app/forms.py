from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, URL, Email, ValidationError
from portfolio_app.models import Portfolio, Project, User
from portfolio_app.extensions import bcrypt

# class UserForm(FlaskForm):
#   """Form for updating User Profile."""
#   username = StringField("Username",
#     validators=[
#       DataRequired(),
#       Length(min=3, max=100, message="Your username must be between 3 and 100 characters.")
#     ])
#   email = StringField("Email",
#     validators=[
#       DataRequired(),
#       Email(message="Please enter a valid URL."),
#       Length(min=5, max=80, message="Your email must be between 5 and 80 characters.")
#     ])
#   submit = SubmitField("Update Profile")

class PortfolioForm(FlaskForm):
  bio = StringField("Bio", 
    validators=[
      DataRequired(),
      Length(min=3, max=100, message="Your bio must be between 3 and 100 characters.")
    ])
  skills = StringField("Skills", 
    validators=[
      DataRequired(),
      Length(min=3, message="Please enter at least 3 characters for skills.")
    ])
  submit = SubmitField("Create Portfolio")


class ProjectForm(FlaskForm):
  title = StringField("Project Title", 
    validators=[
      DataRequired(),
      Length(min=3, max=100, message="Your title must be between 3 and 100 characters.")
    ])
  description = StringField("Project Description", 
    validators=[
      DataRequired(),
      Length(min=3, max=200, message="Description must be between 3 and 200 characters.")
    ])
  github_link = StringField("Github Link", 
    validators=[
      DataRequired(),
      URL(message="Please enter a valid email address.")
    ])
  submit = SubmitField("Add Project")

class SignUpForm(FlaskForm):
  username = StringField('Username',
      validators=[DataRequired(), Length(min=3, max=50)])
  email = StringField("Email",
    validators=[DataRequired(),
      Email(message="Please enter a valid email address."),
      Length(min=5, max=80, message="Your email must be between 5 and 80 characters.")]
  )
  password = PasswordField('Password', validators=[DataRequired()])
  submit = SubmitField('Sign Up')

  def validate_username(self, username):
    user = User.query.filter_by(username=username.data).first()
    if user:
      raise ValidationError('Incorrect username or password.')

class LoginForm(FlaskForm):
  username = StringField('Username',
    validators=[DataRequired(), Length(min=3, max=50)])
  password = PasswordField('Password', validators=[DataRequired()])
  submit = SubmitField('Log In')

  def validate_username(self, username):
    user = User.query.filter_by(username=username.data).first()
    if not user:
      raise ValidationError('Incorrect username or password.')

  def validate_password(self, password):
    user = User.query.filter_by(username=self.username.data).first()
    if user and not bcrypt.check_password_hash(
        user.password, password.data):
      raise ValidationError('Incorrect username or password.')