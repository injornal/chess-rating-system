from datetime import datetime
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
    else:
        return redirect("/login")
    future_tournaments = [t for t in user.tournaments if t.date >= datetime.now()]
    past_tournaments = [t for t in user.tournaments if t.date < datetime.now()]
    print(future_tournaments, past_tournaments)
    return render_template("profile.html", user=user, future_tournaments=future_tournaments, past_tournaments=past_tournaments)


@profile_bp.route("/<int:user_id>")
def public_profile(user_id):
    with Session(engine) as session:
        query = select(Users).where(Users.id == user_id)
        user = session.execute(query).first()[0]
    return render_template("public-profile.html", user=user)
