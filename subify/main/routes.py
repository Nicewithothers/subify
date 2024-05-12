"""Imports"""
from flask import Blueprint, render_template

main = Blueprint('main', __name__)


@main.route('/')
def index():
    """Index site route"""
    return render_template("base.html")
