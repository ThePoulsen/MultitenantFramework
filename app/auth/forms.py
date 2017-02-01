## -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, PasswordField
from wtforms.validators import InputRequired, Email

class setPasswordForm(FlaskForm):
    password = PasswordField('Password', [InputRequired('Please enter a password')])

class changePasswordForm(FlaskForm):
    password = PasswordField('Password,', [InputRequired('Please enter a password')])

class loginForm(FlaskForm):
    regNo = StringField('Registration ID',  [InputRequired('Please enter a Registration ID')])
    email = StringField('Email', [InputRequired("Please enter your email address."), Email("This field requires a valid email address")])
    password = PasswordField('Password', [InputRequired('Please enter a password')])

class registerForm(FlaskForm):
    regNo = StringField('Registration ID',  [InputRequired('Please enter a Registration ID')])
    companyName = StringField('Company name',[InputRequired('Please enter a company name')])
    userName = StringField('User name',[InputRequired('Please enter a user name')])
    email = StringField('Email', [InputRequired("Please enter your email address."), Email("This field requires a valid email address")])
    password = PasswordField('Password', [InputRequired('Please enter a password')])
