from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, Email, EqualTo


class LoginForm(FlaskForm):
    email = StringField('email', validators=[
        InputRequired(message="Mező kitöltése kötelező!"),
        Email(message="Nem megfelelő e-mail formátum!")])
    password = PasswordField('password', validators=[
        InputRequired(message="Mező kitöltése kötelező!"),
        Length(min=4, max=25, message="4 és 25 karakter között kell legyen!")
    ])
    submit = SubmitField('login')


class RegisterForm(FlaskForm):
    email = StringField('email', validators=[
        InputRequired(message="Mező kitöltése kötelező!"),
        Email(message="Nem megfelelő e-mail formátum!")])
    name = StringField('name', validators=[
        InputRequired(message="Mező kitöltése kötelező!")])
    password = PasswordField('password', validators=[
        InputRequired(message="Mező kitöltése kötelező!"),
        Length(min=4, max=25, message="4 és 25 karakter között kell legyen!")
    ])
    password_verify = PasswordField('password_verify', validators=[
        InputRequired(message="Mező kitöltése kötelező!"),
        EqualTo('password', message="Nem egyezik a két jelszó!")
    ])
    submit = SubmitField('register')
