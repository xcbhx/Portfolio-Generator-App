import os
from flask import Blueprint, request, render_template, redirect, url_for


from portfolio_app import app, db

main = Blueprint("main", __name__)

@main.route("/")
def index():
  return render_template("index.html")