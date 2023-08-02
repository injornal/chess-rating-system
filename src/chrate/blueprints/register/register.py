from hashlib import sha256
from flask import request, render_template, blueprints, redirect
from chrate.model.rating import Users, engine
from sqlalchemy.orm import Session

register_bp = blueprints.Blueprint("register", __name__, template_folder="templates", url_prefix="/register")


@register_bp.route("/", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        username = request.form.get("username")
        email = request.form.get("email")
        password = sha256(request.form.get("password").encode()).hexdigest()
        user = Users(firstname=firstname, lastname=lastname, password=password, username=username, email=email)

        with Session(engine) as session:
            session.add(user)
            session.commit()
        return redirect("/auth")
