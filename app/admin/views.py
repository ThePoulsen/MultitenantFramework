## -*- coding: utf-8 -*-

from app import db
from flask import Blueprint, render_template, request, redirect, url_for, session, g
from services import requiredRole, loginRequired

adminBP = Blueprint('adminBP', __name__, template_folder='templates')

# Admin view
@adminBP.route('/')
@requiredRole(u'siteAdmin')
@loginRequired
def adminView():
    kwargs = {'title':'Admin'}

    return render_template('admin/adminView.html', **kwargs)
