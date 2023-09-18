from flask import Flask, flash, redirect, url_for
from chrate.blueprints.profile.profile import profile_bp
from chrate.blueprints.register.register import register_bp
from chrate.blueprints.auth.login import auth_bp
from chrate.blueprints.tournament.game.game import game_bp
from chrate.blueprints.home.home import home_bp
from chrate.blueprints.tournament.tournament import tournament_bp
from chrate.blueprints.admin.admin import admin_bp
from flask_login import LoginManager
from sqlalchemy.orm import Session
from sqlalchemy import select
from chrate.model.rating import Users, engine

app = Flask(__name__)
app.config["SECRET_KEY"] = "Yellow soup"

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = "warning"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    with Session(engine) as session:
        query = select(Users).where(Users.id == user_id)
        user = session.execute(query).first()
        if user is not None:
            user = user[0]
        else:
            flash("User doesn't exist", "warning")
            return redirect(url_for("auth.login"))
    return user


app.register_blueprint(profile_bp)
app.register_blueprint(register_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(game_bp)
app.register_blueprint(home_bp)
app.register_blueprint(tournament_bp)
app.register_blueprint(admin_bp)

