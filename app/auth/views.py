## -*- coding: utf-8 -*-
from flask import Blueprint, session, render_template, url_for, jsonify, json, g, redirect
from app.admin.services import sendMail, loginRequired, logoutUser, requiredRole, successMessage, errorMessage, apiMessage
from forms import registerForm, setPasswordForm, loginForm
import requests
from authAPI import authAPI

authBP = Blueprint('authBP', __name__, template_folder='templates')

# register
@authBP.route('/register')
def registerView():
    if not 'token' in session:
        # universal variables
        form = registerForm()
        kwargs = {'formWidth':400}

        if form.validate_on_submit():
            dataDict = {'regNo' : form.regNo.data,
                        'companyName' : form.companyName.data,
                        'userName' : form.userName.data,
                        'email' : form.email.data,
                        'password' : form.password.data}

            req = authAPI('register', method='post', dataDict=dataDict)

            if r.status_code == 409:
                errorMessage('accountExists')
            elif r.status_code == 404:
                errorMessage('cvrCheckError')
            elif 'error' in req:
                if req['error'] == 'Not valid email-address':
                    errorMessage('validateEmail')
            elif 'success' in req:
                # send email confirmation
                subject = u'Bekræft tilmelding'
                tok = req['token']
                email = req['email']
                confirm_url = url_for('authBP.confirmEmailView',token=tok, _external=True)
                html = render_template('email/verify.html', confirm_url=confirm_url)
    #
                sendMail(subject=subject,
                         sender='Henrik Poulsen',
                         recipients=[email],
                         html_body=html,
                         text_body = None)
                successMessage('loginSuccess')
                return redirect(url_for('indexView'))

        return render_template('auth/registerForm.html', form=form, **kwargs)
    else:
        errorMessage('alreadyRegistered')
        return redirect(url_for('indexView'))

# Confirmation mail redirect
@authBP.route('/confirm/<token>')
def confirmEmailView(token):
    session.clear()
    req = authAPI('confirm', method='post', token=token)
    if 'error' in req:
        if req['error'] == 'User already confirmed':
            if req['mustSetPass'] == 'True':
                successMessage('Account confirmed, please set new password (the password your enter here will be your new password to the system)')
                return redirect(url_for('authBP.setPasswordView', tok=req['token']))
            else:
                errorMessage('Your profile has already been confirmed')
        else:
            errorMessage(req['error'])

    elif 'success' in req:
        if req['mustSetPass'] == 'True':
            return redirect(url_for('authBP.setPasswordView', tok=req['token']))
        else:
            successMessage('Your profile has already been confirmed')
            return redirect(url_for('authBP.loginView'))

    return redirect(url_for('indexView'))

# Set password

@authBP.route('/setPassword/<string:tok>', methods=['GET','POST'])
def setPasswordView(tok):
    session.clear()
    kwargs = {'formWidth':300,
              'title':'Set new password'}

    form = setPasswordForm()

    if form.validate_on_submit():
        dataDict={'password':form.password.data}

        req = authAPI('setPassword', method='post', dataDict=dataDict, token=tok)

        print str(req)

        if 'error' in req:
            errorMessage(req['error'])
        elif 'success' in req:
            successMessage('Your password has now been set, please login')
            return redirect(url_for('authBP.loginView'))

    return render_template('auth/setPasswordForm.html', form=form, **kwargs)

# Login
@authBP.route('/login', methods=['GET','POST'])
def loginView():
    if not 'token' in session:
        kwargs = {'formWidth':300,
                  'contentTitle':'Login'}

        form = loginForm()
        if form.validate_on_submit():
            regNo = form.regNo.data
            email = form.email.data
            password = form.password.data

            dataDict = {'regNo':regNo,
                        'email':email,
                        'password':password}

            req = authAPI('login', method='post', dataDict=dataDict)
            if 'success' in req:
                session['token'] = req['token']
                session['email'] = req['email']
                session['roles'] = req['roles']
                successMessage('You are now logged in')
                return redirect(url_for('indexView'))
            else:
                errorMessage('User / password combination error')

        return render_template('auth/loginForm.html', form=form, **kwargs)
    else:
        errorMessage('You are already logged into the system')
        return redirect(url_for('indexView'))

# Logout
@authBP.route('/logout', methods=['GET','POST'])
def logoutView():
    logoutUser()
    return redirect(url_for('indexView'))
