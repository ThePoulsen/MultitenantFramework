## -*- coding: utf-8 -*-
## project/app/settings/views.py

from flask import Blueprint, render_template, url_for, g, request, redirect, session, json
from app.admin.services import requiredRole, loginRequired
from app import db
from forms import companyForm
from authAPI import authAPI

settingsBP = Blueprint('settingsBP', __name__, template_folder='templates')

@settingsBP.route('/company')
@requiredRole(u'Administrator')
@loginRequired
def companyView():
    form = companyForm()
    kwargs = {'title':'title',
              'formWidth':'350'}
    return render_template('settings/companyView.html', form=form, **kwargs)

@settingsBP.route('/settings')
@requiredRole(u'Administrator')
@loginRequired
def settingsView():
    kwargs = {'title':'title',
              'formWidth':'350'}
    return render_template('settings/settingsView.html', **kwargs)
