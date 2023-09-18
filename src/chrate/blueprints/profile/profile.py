from datetime import datetime
from flask import blueprints, render_template, session as flask_session, redirect, url_for, flash
from chrate.model.rating import Users, engine, Tournaments
from sqlalchemy.orm import Session
from sqlalchemy import select
from flask_login import login_required, current_user

profile_bp = blueprints.Blueprint("profile", __name__, template_folder="templates", url_prefix="/profile")


@profile_bp.route("/")
@login_required
def profile():
    with Session(engine) as session:
        query = select(Users).where(Users.id == current_user.id)
        user = session.execute(query).first()
        if user:
            user = user[0]
        else:
            return redirect(url_for("auth"))
    future_tournaments = [t for t in user.tournaments if t.date >= datetime.now()]
    past_tournaments = [t for t in user.tournaments if t.date < datetime.now()]
    return render_template("profile.html", user=user, future_tournaments=future_tournaments, past_tournaments=past_tournaments)


@profile_bp.route("/<int:user_id>")
def public_profile(user_id):
    with Session(engine) as session:
        query = select(Users).where(Users.id == user_id)
        user = session.execute(query).first()
        if user is not None:
            user = user[0]
        else:
            flash("User doesn't exist", "warning")
            return redirect(url_for("home.home"))
    return render_template("public-profile.html", user=user)
