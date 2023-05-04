from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_mysqldb import MySQL
from Website import app, db  # initially created by __init__.py, need to be used here


@app.route("/")
def index():
    return render_template("landing.html", pageTitle="Landing Page")

@app.route("/sign-up")
def sign_up():
    return render_template("sign_up.html")

@app.route("/login")
def login():
    return render_template("login.html")

