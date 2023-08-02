from flask import blueprints, render_template
from flask_login import login_required

admin_bp = blueprints.Blueprint("admin", __name__, template_folder="templates", url_prefix="/admin")


@admin_bp.route("/")
@login_required
def admin():
    return render_template("admin.html")
