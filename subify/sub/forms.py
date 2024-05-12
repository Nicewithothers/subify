"""Imports"""
from flask_wtf import FlaskForm
from wtforms import (StringField, SelectField, IntegerField,
                     BooleanField, SubmitField)
from wtforms.validators import InputRequired, Length, NumberRange


class NewSubForm(FlaskForm):
    """New sub form"""
    name = StringField('Name', validators=[
        InputRequired(message="You must type a name!"),
        Length(min=2, message="You must type a name longer"
                              "than 2 characters!"),
    ])
    type = SelectField('type', default='streaming', choices=[
        ('streaming', 'Streaming'),
        ('groceries', 'Groceries'),
        ('bills', 'Taxes/bills'),
        ('meals', 'Meals'),
        ('other', 'Miscellaneous')
    ], validators=[InputRequired(message="You must select a type!")])
    occurance_type = SelectField('type', default='onetime', choices=[
        ('onetime', 'One-time'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly')
    ], validators=[
        InputRequired(message="You must select an"
                              "occurance type!")])
    price = IntegerField('price', validators=[
        InputRequired("You must enter a price!"),
        NumberRange(min=100, message="Expense cannot be lower than 100!")
    ])
    is_paid = BooleanField('is_paid')
    submit = SubmitField('Add')
