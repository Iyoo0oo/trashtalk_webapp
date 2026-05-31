from flask import Flask, render_template, request, redirect, session

from config import ADMIN, WASTE
from services.auth import register, login
from services.waste import add, process, get_all
from services.storage import init, update_rewards, write

app = Flask(__name__)
app.secret_key = "clean_key"

init()


@app.route("/")
def home():
    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def reg():
    if request.method == "POST":
        register(request.form["user"], request.form["pass"])
        return redirect("/login")
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def log():
    if request.method == "POST":

        u = request.form["user"]
        p = request.form["pass"]

        if u == ADMIN["username"] and p == ADMIN["password"]:
            session["user"] = u
            session["admin"] = True
            return redirect("/admin")

        if login(u, p):
            session["user"] = u
            session["admin"] = False
            return redirect("/dashboard")

    return render_template("index.html")


@app.route("/dashboard", methods=["GET", "POST"])
def dash():
    if "user" not in session:
        return redirect("/login")

    if session.get("admin"):
        return redirect("/admin")

    if request.method == "POST":

        p = add(
            session["user"],
            request.form["address"],
            request.form["category"],
            request.form["sub"],
            float(request.form["weight"])
        )

        if p:
            write("data/history.csv",
                  [p.user, p.category, p.sub, p.weight])

            update_rewards(p.user, int(p.weight * 10))

    return render_template(
        "dashboard.html",
        queue=get_all(),
        categories=WASTE
    )


@app.route("/admin", methods=["GET", "POST"])
def admin():
    if not session.get("admin"):
        return redirect("/login")

    if request.method == "POST":
        process()

    return render_template("admin.html", queue=get_all())


@app.route("/rewards")
def rewards():
    from services.storage import read
    return render_template("rewards.html",
                           rewards=read("data/rewards.csv"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)