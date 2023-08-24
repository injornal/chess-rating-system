from flask import blueprints, request, render_template, redirect, session as flask_session, flash, url_for
from chrate.model.rating import Users, engine
from sqlalchemy import select
from sqlalchemy.orm import Session
from hashlib import sha256
from flask_login import login_user, logout_user, login_required

auth_bp = blueprints.Blueprint("auth", __name__, template_folder="templates", url_prefix="/auth")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        email = request.form.get("email")
        password = sha256(request.form.get("password").encode()).hexdigest()
        with Session(engine) as session:
            query = select(Users).where(Users.email == email)
            user = session.execute(query).first()[0]

        if user and user.password == password:
            login_user(user)
            return redirect(url_for("profile.profile"))
        else:
            flash("Wrong password or username", "warning")
            return render_template("login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home.home"))
