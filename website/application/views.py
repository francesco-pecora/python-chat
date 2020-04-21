from flask import Blueprint
from flask import Flask, render_template, url_for, redirect, request, session, jsonify, flash, Blueprint
from .database import DataBase

view = Blueprint("views", __name__)

NAME_KEY = "name"
MSG_LIMIT = 20


@view.route("/login", methods=["POST", "GET"])
def login():
    """
    Adds user to the session and redirects to home.
    """
    if request.method == "POST":
        name = request.form["inputName"]
        if len(name) >= 2:
            session[NAME_KEY] = name
            flash(f"You were successfully logged in as {name}.")
            return redirect(url_for("views.home"))
        else:
            flash("1Name must be longer than 1 character.")
        
    return render_template("login.html", **{"session": "session"})


@view.route("/logout")
def logout():
    """
    Removes the users from the session and redirects to the login page.
    """
    session.pop(NAME_KEY, None)
    flash("0You were logged out.")
    return redirect(url_for("views.login"))


@view.route("/")
@view.route("/home")
def home():
    """
    Renders the home page. If the user is not registered, it redirects to the login page.
    """
    if NAME_KEY not in session:
        return redirect(url_for("views.login"))
    
    return render_template("index.html", **{"session": session})


@view.route("/history")
def history():
    """
    If user is in the session, shows the history of all the messages sent by the user.
    """
    if NAME_KEY not in session:
        flash("0Please login before viewing message history")
        return redirect(url_for("views.login"))
    json_messages = get_history(session[NAME_KEY])
    return render_template("history.html", **{"history": json_messages})


@view.route("/get_name")
def get_name():
    """
    Get the name of the user, if in the session
    :return: Json
    """
    data = {"name": ""}
    if NAME_KEY in session:
        data = {"name": session[NAME_KEY]}
    return jsonify(data)


@view.route("/get_messages")
def get_messages():
    """
    Get the messages from the database
    :return: Json
    """
    db = DataBase()
    msgs = db.get_all_messages(MSG_LIMIT)
    messages = remove_seconds_from_messages(msgs)

    return jsonify(messages)


@view.route("/get_history")
def get_history(name):
    """
    Get the messages from only one user.
    :return: []
    """
    db = DataBase()
    msgs = db.get_all_messages_by_name(name)
    messages = remove_seconds_from_messages(msgs)

    return messages


def remove_seconds_from_messages(msgs):
    """
    Loops through the messages and removes the seconds
    :param msgs: []
    :return: []
    """
    messages = []
    for msg in msgs:
        message = msg
        message["time"] = remove_seconds(message["time"])
        messages.append(message)

    return messages

def remove_seconds(msg):
    """
    Removes seconds from a single message
    :param msg: {}
    :return: string
    """
    return msg.split(".")[0][:-3]