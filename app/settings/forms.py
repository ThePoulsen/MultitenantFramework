## -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SelectMultipleField, BooleanField, IntegerField
from app.admin.services import select2Widget, select2MultipleWidget
from wtforms.validators import InputRequired, Email

class companyForm(FlaskForm):
    regNo = StringField('Registration ID',  [InputRequired('Please enter a Registration ID')])
    companyName = StringField('Company name',[InputRequired('Please enter a company name')])
    addr = StringField('Address')
    addr2 = StringField('Address 2')
    postcode = StringField('Postal code')
    city = StringField('City')
    contactName = SelectField('Contact name', choices=[])
    email = StringField('Email', [InputRequired("Please enter your email address."), Email("This field requires a valid email address")])
    phone = IntegerField('Phone number')
