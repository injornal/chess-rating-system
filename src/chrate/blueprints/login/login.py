from flask import blueprints, request, render_template, redirect, session as flask_session, flash
from chrate.model.rating import Users, engine
from sqlalchemy import select
from sqlalchemy.orm import Session
from hashlib import sha256

login_bp = blueprints.Blueprint("login", __name__, template_folder="templates", url_prefix="/login")


@login_bp.route("/", methods=["GET", "POST"])
def sign_in():
    if request.method == "GET":
        return render_template("login.html")
    else:
        email = request.form.get("email")
        password = sha256(request.form.get("password").encode()).hexdigest()
        with Session(engine) as session:
            query = select(Users).where(Users.email == email)
            user = session.execute(query).first()
            if user:
                user = user[0]

        if user and user.password == password:
            flask_session["user_id"] = user.id
            return redirect("/profile")
        else:
            flash("Wrong password or username", "warning")
            return render_template("login.html")


@login_bp.route("/logout")
def logout():
    del flask_session["user_id"]
    return redirect("/")
