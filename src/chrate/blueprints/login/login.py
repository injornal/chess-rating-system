from flask import blueprints, request, render_template, redirect
from chrate.model.rating import User, engine
from sqlalchemy import select
from sqlalchemy.orm import Session
from hashlib import sha256

login_bp = blueprints.Blueprint("login", __name__, template_folder="templates", static_folder='static',
                                url_prefix="/login")


@login_bp.route("/", methods=["GET", "POST"])
def sign_in():
    if request.method == "GET":
        return render_template("login.html")
    else:
        email = request.form.get("email")
        password = sha256(request.form.get("password").encode()).hexdigest()
        with Session(engine) as session:
            query = select(User).where(User.email == email)
            user = session.execute(query).first()
            if user:
                user = user[0]

        if user and user.password == password:
            return redirect("/profile")
        else:
            return render_template("login.html", message="wrong username or password")
