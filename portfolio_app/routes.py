import os
from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import datetime
from portfolio_app.models import User, Portfolio, Project

from portfolio_app import app, db

main = Blueprint("main", __name__)

@main.route("/")
def homepage():
  """Landing page explaing what the app does."""
  return render_template("index.html")


@main.route("/create_portfolio", methods=["GET", "POST"])
def create():
  """ Create a new porfolio."""
  if request.method == "POST":
    new_bio = request.form.get("bio")
    new_skills = request.form.get("skills")
    new_projects = request.form.get("projects")
    created_at = request.form.get("created_at")

    try:
      created_at = datetime.strftime(
        f'{created_at}',
        "%Y-%m-%d %H:%M")
    except ValueError:
      return render_template("create_porfolio.html",
        error="Incorrect datetime format! Please try again.")
    
    new_portfolio = Portfolio(
      bio=new_bio,
      skills=new_skills,
      projects=new_projects,
      created_at=created_at
    )
    db.session.add(new_portfolio)
    db.session.commit()

    flash("Portfolio Created.")
    return redirect(url_for("main.display"))
  else:
    return render_template("create_portfolio.html")

@main.route("/portfolio/<portfolio_id>", methods=["GET"])
def portfolio_detail(portfolio_id):
  """Show portfolio."""
  portfolio = Portfolio.query.get(portfolio_id)
  return render_template("portfolio_detail.html", portfolio=portfolio)



@main.route("/portfolio/<project_id>", methods=["GET"])
def project_detail(project_id):
  """Show project."""
  project = Project.query.get(project_id)
  return render_template("project_detail.html", project=project)

