## -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, PasswordField, BooleanField, SelectMultipleField, RadioField, validators, SubmitField
from wtforms.validators import InputRequired, Email
from app.admin.services import  select2MultipleWidget

class changePasswordForm(FlaskForm):
    password = PasswordField('New password', [InputRequired('Please enter a password')])

class userForm(FlaskForm):
    userName = StringField('Name', validators=[InputRequired('Please enter a user name')])
    userEmail = StringField('Email', [InputRequired("Please enter your email address."), Email("This field requires a valid email address")])
    userPhone = StringField('Phone number')
    userRole = RadioField('User role', choices=[('Administrator','Administrator'),('Superuser','Superuser'),('User','User')])
    userGroups = SelectMultipleField('Group memberships', choices=[], widget=select2MultipleWidget())
    userSubmit = SubmitField('OK')

class groupForm(FlaskForm):
    groupName = StringField('Name', validators=[InputRequired('Please enter a group name')])
    groupDesc = TextAreaField('Description')
    groupUsers = SelectMultipleField('Users', validators=[], choices=[], widget=select2MultipleWidget(), _name='test')
    groupSubmit = SubmitField('OK')
