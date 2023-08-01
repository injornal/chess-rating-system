from flask import Flask
from chrate.blueprints.profile.profile import profile_bp
from chrate.blueprints.register.register import register_bp
from chrate.blueprints.login.login import login_bp
from chrate.blueprints.tournament.game.game import game_bp
from chrate.blueprints.home.home import home_bp
from chrate.blueprints.tournament.tournament import tournament_bp
from chrate.blueprints.admin.admin import admin_bp


app = Flask(__name__)
app.config["SECRET_KEY"] = "Yellow soup"

app.register_blueprint(profile_bp)
app.register_blueprint(register_bp)
app.register_blueprint(login_bp)
app.register_blueprint(game_bp)
app.register_blueprint(home_bp)
app.register_blueprint(tournament_bp)
app.register_blueprint(admin_bp)

