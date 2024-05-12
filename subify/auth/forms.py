"""Imports"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, Email, EqualTo


class LoginForm(FlaskForm):
    """Login form"""
    email = StringField('email', validators=[
        InputRequired(message="You must type something here!"),
        Email(message="Invalid email format!")])
    password = PasswordField('password', validators=[
        InputRequired(message="You must type something here!"),
        Length(min=4, max=25, message="Invalid pw length!")
    ])
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    """Register form"""
    email = StringField('email', validators=[
        InputRequired(message="You must type something here!"),
        Email(message="Invalid email format!")])
    name = StringField('name', validators=[
        InputRequired(message="You must type something here!")])
    password = PasswordField('password', validators=[
        InputRequired(message="You must type something here!"),
        Length(min=4, max=25, message="Invalid pw length!")
    ])
    password_verify = PasswordField('password_verify', validators=[
        InputRequired(message="You must type something here!"),
        EqualTo('password', message="Passwords do not match!")
    ])
    submit = SubmitField('Register')
