from flask import Blueprint
from flask import Flask, render_template, url_for, redirect, request, session, jsonify, flash, Blueprint
from .database import DataBase

view = Blueprint("views", __name__)

NAME_KEY = "name"
MSG_LIMIT = 20


@view.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        name = request.form["inputName"]
        if len(name) >= 2:
            session[NAME_KEY] = name
            flash(f"You were successfully logged in as {name}.")
            return redirect(url_for("views.home"))
        else:
            flash("Name must be longer than 1 character.")
        
    return render_template("login.html", **{"session": "session"})


@view.route("/logout")
def logout():
    session.pop(NAME_KEY, None)
    flash("You were logged out.")
    return redirect(url_for("views.login"))


@view.route("/")
@view.route("/home")
def home():
    if NAME_KEY not in session:
        return redirect(url_for("views.login"))
    
    return render_template("index.html", **{"session": session})


@view.route("/get_name")
def get_name():
    data = {"name": ""}
    if NAME_KEY in session:
        data = {"name": session[NAME_KEY]}
    return jsonify(data)


@view.route("/get_messages")
def get_messages():
    db = DataBase()
    msgs = db.get_all_messages(MSG_LIMIT)
    messages = []
    for msg in msgs:
        message = msg
        message["time"] = remove_seconds(message["time"])
        messages.append(message)

    return jsonify(msgs)

def remove_seconds(msg):
    return msg.split(".")[0][:-3]