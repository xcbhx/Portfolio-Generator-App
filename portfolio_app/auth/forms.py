from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from portfolio_app.models import User
from portfolio_app.extensions import bcrypt


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