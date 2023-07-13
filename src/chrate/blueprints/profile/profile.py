from flask import blueprints, render_template, session as flask_session
from chrate.model.rating import User, engine
from sqlalchemy.orm import Session
from sqlalchemy import select

profile_bp = blueprints.Blueprint("profile", __name__, template_folder="templates", url_prefix="/profile")


@profile_bp.route("/")
def profile():
    if "user_id" in flask_session:
        with Session(engine) as session:
            query = select(User).where(User.id == flask_session["user_id"])
            user = session.execute(query).first()[0]
    return render_template("profile.html", username=user.username)
