from flask import blueprints, render_template

admin_bp = blueprints.Blueprint("admin", __name__, template_folder="templates", url_prefix="/admin")


@admin_bp.route("/")
def admin():
    return render_template("admin.html")
