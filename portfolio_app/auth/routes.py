from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user

from portfolio_app.models import User
from portfolio_app.forms import SignUpForm, LoginForm

from portfolio_app.extensions import db, bcrypt

auth = Blueprint("auth", __name__)

@auth.route("/signup", methods=["GET", "POST"])
def signup():
  form = SignUpForm()
  if form.validate_on_submit():
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
    user = User(
      username=form.username.data,
      email=form.email.data,
      password=hashed_password
    )
    db.session.add(user)
    db.session.commit()

    flash("Account Created.")
    return redirect(url_for("auth.login"))
  return render_template("auth/signup.html", form=form)


@auth.route("/login", methods=["GET", "POST"])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data).first()
    if user and bcrypt.check_password_hash(user.password, form.password.data):
      login_user(user, remember=True)
      flash("Logged in successfully.")
      next_page = request.args.get("next")
      return redirect(next_page if next_page else url_for("main.create"))
    else:
      flash("Invalid username or password.")
  return render_template("auth/login.html", form=form)


@auth.route("/logout")
@login_required
def logout():
  logout_user()
  return redirect(url_for("main.homepage"))