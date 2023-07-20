from flask import blueprints, render_template, session as flask_session, redirect
from chrate.model.rating import Users, engine, Tournaments
from sqlalchemy.orm import Session
from sqlalchemy import select

profile_bp = blueprints.Blueprint("profile", __name__, template_folder="templates", url_prefix="/profile")


@profile_bp.route("/")
def profile():
    if "user_id" in flask_session:
        with Session(engine) as session:
            query = select(Users).where(Users.id == flask_session["user_id"])
            user = session.execute(query).first()
            if user:
                user = user[0]
            else:
                return redirect("/login")
    return render_template("profile.html", user=user)
