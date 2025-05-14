from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, URL

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
  submit = SubmitField("Save Portfolio")


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