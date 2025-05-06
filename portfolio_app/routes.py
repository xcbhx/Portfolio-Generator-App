import os
from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import datetime
from portfolio_app.models import User, Portfolio, Project
from portfolio_app.forms import PortfolioForm

from portfolio_app import db

main = Blueprint("main", __name__)

@main.route("/")
def homepage():
  """Landing page explaing what the app does."""
  return render_template("index.html")


@main.route("/create_portfolio", methods=["GET", "POST"])
def create():
  """ Create a new porfolio."""
  form = PortfolioForm()

  if  form.validate_on_submit():
    #  Handles dynamic skills fields from the form
    skills_list = request.form.getlist("skills")
    skills_combined = ", ".join(skills_list)

    new_portfolio = Portfolio(
      bio=form.bio.data,
      skills=skills_combined
    )
    
    db.session.add(new_portfolio)
    db.session.commit()

    flash("Portfolio Created.")
    return redirect(url_for("main.portfolio_detail", portfolio_id=new_portfolio.id))
  else:
    return render_template("create_portfolio.html", form=form)

@main.route("/portfolio/<int:portfolio_id>", methods=["GET"])
def portfolio_detail(portfolio_id):
  """Show portfolio."""
  portfolio = Portfolio.query.get(portfolio_id)
  return render_template("portfolio_detail.html", portfolio=portfolio)



@main.route("/project/<int:project_id>", methods=["GET"])
def project_detail(project_id):
  """Show project."""
  project = Project.query.get(project_id)
  return render_template("project_detail.html", project=project)

