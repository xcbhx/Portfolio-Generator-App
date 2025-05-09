from flask import Blueprint, request, render_template, redirect, url_for, flash
from portfolio_app.models import User, Portfolio, Project
from portfolio_app.forms import PortfolioForm, ProjectForm
from flask_login import login_required, current_user

from portfolio_app import db

main = Blueprint("main", __name__)

@main.route("/")
def homepage():
  """Landing page explaing what the app does."""
  return render_template("main/index.html")


@main.route("/create_portfolio", methods=["GET", "POST"])
@login_required
def create():
  """ Create a new porfolio."""
  form = PortfolioForm()

  if  form.validate_on_submit():
    #  Handles dynamic skills fields from the form
    skills_list = request.form.getlist("skills")
    skills_combined = ", ".join(skills_list)

    new_portfolio = Portfolio(
      bio=form.bio.data,
      skills=skills_combined,
      user=current_user
    )
    
    db.session.add(new_portfolio)
    db.session.commit()

    flash("Portfolio Created.")
    return redirect(url_for("main.portfolio_detail", portfolio_id=new_portfolio.id))
  else:
    return render_template("main/create_portfolio.html", form=form)

@main.route("/portfolio/<int:portfolio_id>", methods=["GET"])
@login_required
def portfolio_detail(portfolio_id):
  """Display a single portfolio's details."""
  portfolio = Portfolio.query.get_or_404(portfolio_id)
  return render_template("main/portfolio_detail.html", portfolio=portfolio)

@main.route("/portfolio/<int:portfolio_id>/edit", methods=["GET", "POST"])
@login_required
def edit_portfolio(portfolio_id):
  """Display form to edit portfolio."""
  portfolio = Portfolio.query.get_or_404(portfolio_id)
  # Pre-fill the form using obj=portfolio
  form = PortfolioForm(obj=portfolio)

  if form.validate_on_submit():
    # Update the porfolio with new form data
    portfolio.bio = form.bio.data
    # Dynamically display skill input
    skills_list = request.form.getlist("skills")
    portfolio.skills = ", ".join(skills_list)

    db.session.commit()

    flash("Portfolio details updated successfully.")
    return redirect(url_for("main.portfolio_detail", portfolio_id=portfolio.id))

  return render_template("main/edit_portfolio.html", portfolio=portfolio, form=form)


@main.route("/portfolio/<int:portfolio_id>/create_project", methods=["GET", "POST"])
@login_required
def create_project(portfolio_id):
  """Displaying form to add one or more projects to portfolio."""
  form = ProjectForm()

  if request.method == "POST":
    titles = request.form.getlist("project_title")
    descriptions = request.form.getlist("project_description")
    github_links = request.form.getlist("project_github")

    if not all(titles) or not all(github_links):
      flash("Each project must include a title and Github link.")
      return redirect(request.url)
    
    for title, desc, link in zip(titles, descriptions, github_links):
      new_project = Project(
        portfolio_id=portfolio_id,
        title=title,
        description=desc,
        github_link=link
      )
      db.session.add(new_project)

    db.session.commit()

    flash("New project was created successfully.")
    return redirect(url_for("main.portfolio_detail", portfolio_id=portfolio_id))

  return render_template("main/create_project.html", form=form)


@main.route("/project/<int:project_id>", methods=["GET"])
@login_required
def project_detail(project_id):
  """Display projects."""
  project = Project.query.get_or_404(project_id)
  return render_template("project_detail.html", project=project)


@main.route("/portfolio/<int:portfolio_id>/edit_projects", methods=["GET", "POST"])
@login_required
def edit_projects(portfolio_id):
  """Display form to edit projects."""
  portfolio = Portfolio.query.get_or_404(portfolio_id)
  projects = portfolio.project_list

  if request.method == "POST":
    titles = request.form.getlist("title")
    descriptions = request.form.getlist("description")
    github_links = request.form.getlist("github_link")
    project_ids = request.form.getlist("project_id")

    for i in range(len(project_ids)):
      project = Project.query.get(int(project_ids[i]))
      project.title = titles[i]
      project.description = descriptions[i]
      project.github_link = github_links[i]

    db.session.commit()

    flash("All project updated successfully.")
    return redirect(url_for("main.portfolio_detail", portfolio_id=portfolio_id))
  
  return render_template("main/edit_project.html", projects=projects, portfolio=portfolio)


@main.route("/project/<int:project_id>/delete", methods=["POST"])
@login_required
def delete_projects(project_id):
  """Delete a project by its ID."""
  project = Project.query.get_or_404(project_id)
  portfolio_id = project.portfolio_id  # Save before deletion

  db.session.delete(project)
  db.session.commit()

  flash("Project deleted successfully.")
  return redirect(url_for("main.portfolio_detail", portfolio_id=portfolio_id))
