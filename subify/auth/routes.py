"""Imports"""
from flask import Blueprint, request, redirect, render_template, flash, url_for
from flask_login import login_required, logout_user, login_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from subify.auth.forms import LoginForm, RegisterForm
from subify.models import User
from subify import database

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Login route"""
    login_form = LoginForm(request.form)
    if login_form.validate_on_submit() and request.method == 'POST':
        email = login_form.email.data
        password = login_form.password.data

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('main.index'))
        else:
            flash("Invalid e-mail address. Please try again!",
                  category='error')
            return redirect(url_for('auth.login'))

    return render_template("login.html", form=login_form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """Register route"""
    reg_form = RegisterForm(request.form)
    if reg_form.validate_on_submit() and request.method == 'POST':
        email = reg_form.email.data
        name = reg_form.name.data
        password = reg_form.password.data

        if User.query.filter_by(email=email).first() == email:
            flash("E-mail address already in use. Try again!",
                  category='error')
            return redirect(url_for('auth.register'))

        user = User(email=email,
                    name=name,
                    password=generate_password_hash(password))

        database.session.add(user)
        database.session.commit()

        login_user(user)

        return redirect(url_for('sub.dashboard', current_user=current_user))

    return render_template("register.html", form=reg_form)


@auth.route('/logout')
@login_required
def logout():
    """Logout route"""
    logout_user()
    return redirect(url_for('main.index'))
