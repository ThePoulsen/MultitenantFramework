## -*- coding: utf-8 -*-

from flask import Blueprint, session, render_template, url_for, jsonify, json, g, redirect, request
from app.admin.services import loginRequired, requiredRole, errorMessage, successMessage, apiMessage, sendMail
from forms import changePasswordForm, userForm, groupForm
import requests, flask_sijax
from app.sijax.handler import SijaxHandler
from authAPI import authAPI
from groupCRUD import getGroups, postGroup, deleteGroup, getGroup, putGroup
from userCRUD import getUsers, getUser, postUser, putUser, deleteUser

userBP = Blueprint('userBP', __name__, template_folder='templates')

# User profile
@userBP.route('/profile', methods=['GET'])
@requiredRole('User')
@loginRequired
def userProfileView():
    kwargs = {'title':'User profile'}

    return render_template('user/userProfileView.html', **kwargs)

@userBP.route('/changePassword', methods=['GET','POST'])
@requiredRole('User')
@loginRequired
def changePasswordView():
    kwargs = {'formWidth':300,
              'contentTitle':'Change password'}

    form = changePasswordForm()

    if form.validate_on_submit():

        dataDict = {'password':form.password.data}

        req = authAPI(endpoint='changePassword', method='put', dataDict=dataDict, token=session['token'])
        apiMessage(req)

    return render_template('user/changePasswordForm.html', form=form, **kwargs)

# Reset password
@userBP.route('/resetPassword', methods=['GET','POST'])
@requiredRole('User')
@loginRequired
def resetPasswordView():
    pass

@flask_sijax.route(userBP, '/user', methods=['GET'])
@flask_sijax.route(userBP, '/user/<string:function>', methods=['GET', 'POST'])
@flask_sijax.route(userBP, '/user/<string:function>/<int:id>', methods=['GET', 'POST'])
@requiredRole(u'Administrator')
@loginRequired
def userView(id=None, function=None):
    # universal variables
    form = userForm()
    kwargs = {'title':'Users',
              'width':'',
              'formWidth':'400'}

    # Get users
    if function == None:
        users = getUsers(includes=['includeRoles', 'includeGroups'])['users']

        tableData = []
        for u in users:
            roles = ''
            for r in u['roles']:
                roles = roles + str(r['title']) +'<br>'
            groups = ''
            for gr in u['groups']:
                groups = groups + str(gr['name']) +'<br>'
            temp = [u['id'],u['name'],u['email'], roles, groups]
            tableData.append(temp)

        kwargs['tableColumns'] =['User name','Email','Roles','Groups']
        kwargs['tableData'] = tableData

        return render_template('listView.html', **kwargs)
    elif function == 'delete':
        delUsr = deleteUser(id)
        apiMessage(delUsr)

        return redirect(url_for('userBP.userView'))
    else:
        if function == 'update':
            usr = getUser(id=id, includes=['includeRoles', 'includeGroups'])['user']
            kwargs['contentTitle'] = 'Update user'
            role = 'User'
            for r in usr['roles']:
                if r['title'] == 'Administrator':
                    role = 'Administrator'
                elif r['title'] == 'Superuser':
                    role = 'Superuser'
            grpForm = groupForm()
            usrForm = userForm(name = usr['userName'],
                            email = usr['userEmail'],
                            phone = usr['userPhone'],
                            groups = [str(r['id']) for r in usr['userGroups']],
                            role = role)

            # Get all groups
            usrForm.groups.choices = [(str(r['id']),r['name']) for r in getGroups()['userGroups']]

            if g.sijax.is_sijax_request:
                g.sijax.register_object(SijaxHandler)
                return g.sijax.process_request()

            if usrForm.validate_on_submit():
                dataDict = {'name':usrForm.userName.data,
                            'email':usrForm.userEmail.data,
                            'phone':usrForm.userPhone.data}

                roles = ['User']
                if usrForm.userRole.data == 'Superuser':
                    roles.append('Superuser')
                elif usrForm.userRole.data == 'Administrator':
                    roles.append('Superuser')
                    roles.append('Administrator')

                dataDict['userRoles'] = roles
                dataDict['userGroups'] = usrForm.userGroups.data
                updateUser = putUser(dataDict=dataDict, id=id)
                if not 'error' in updateUser:
                    apiMessage(updateUser)
                    return redirect(url_for('userBP.userView'))
                else:
                    apiMessage(updateUser)

            return render_template('user/userForm.html', usrForm=usrForm, grpForm=grpForm, **kwargs)
        elif function == 'new':
            usrForm = userForm(userRole='User')
            grpForm = groupForm()
            grpForm.groupUsers.choices = [(str(r['id']),r['email']) for r in getUsers()['users']]
            kwargs['contentTitle'] = 'New user'
            groups = [(str(r['id']),r['name']) for r in getGroups()['groups']]
            usrForm.userGroups.choices = groups

            if g.sijax.is_sijax_request:
                g.sijax.register_object(SijaxHandler)
                return g.sijax.process_request()

            if usrForm.validate_on_submit():
                dataDict = {'name':usrForm.userName.data,
                            'email':usrForm.userEmail.data,
                            'phone':usrForm.userPhone.data}

                roles = ['User']
                if usrForm.userRole.data == 'Superuser':
                    roles.append('Superuser')
                elif usrForm.userRole.data == 'Administrator':
                    roles.append('Superuser')
                    roles.append('Administrator')

                dataDict['roles'] = roles
                dataDict['groups'] = usrForm.userGroups.data
                newUser = postUser(dataDict)
                if not 'error' in newUser:
                    apiMessage(newUser)
                    subject = u'Confirm signup'
                    confirm_url = url_for('authBP.confirmEmailView',token=newUser['token'], _external=True)
                    html = render_template('email/verify.html', confirm_url=confirm_url)

                    sendMail(subject=subject,
                         sender='Henrik Poulsen',
                         recipients=[usrForm.userEmail.data],
                         html_body=html,
                         text_body = None)


                    return redirect(url_for('userBP.userView'))
                else:
                    apiMessage(newUser)
            return render_template('user/userForm.html', usrForm=usrForm, grpForm=grpForm, **kwargs)

    return render_template('listView.html', **kwargs)

# Group View
@userBP.route('/group', methods=['GET'])
@userBP.route('/group/<string:function>', methods=['GET', 'POST'])
@userBP.route('/group/<string:function>/<int:id>', methods=['GET', 'POST'])
@loginRequired
@requiredRole(u'Administrator')
def groupView(function=None, id=None):
    # global variables
    kwargs = {'title':'User groups',
              'width':'600',
              'formWidth':'350',
              'tableColumns':['User group','Description' ,'Users assigned to group']}

    if function == None:
        # perform API request
        req = getGroups(includes=['includeUsers'])['groups']

        # set data for listView
        kwargs['tableData'] = [[r['id'],r['name'], r['desc'],len(r['users'])] for r in req]

        # return view
        return render_template('listView.html', **kwargs)
    elif function == 'delete':
        delGroup = deleteGroup(id)
        apiMessage(delGroup)

        return redirect(url_for('userBP.groupView'))

    else:
        if function == 'update':
            # Get single group
            grp = getGroup(id, includes=['includeUsers'])
            form = groupForm(groupName=grp['name'],
                             groupDesc=grp['desc'],
                             groupUsers = [str(r['id']) for r in grp['users']])
            form.groupUsers.choices = [(str(r['id']),r['email']) for r in getUsers()['users']]
            if form.validate_on_submit():
                dataDict = {'name':form.groupName.data,
                            'desc':form.groupDesc.data,
                            'users':[int(r) for r in form.groupUsers.data]}
                updateGroup = putGroup(dataDict=dataDict, id=id)
                if 'error' in updateGroup:
                    apiMessage(updateGroup)
                else:
                    apiMessage(updateGroup)
                    return redirect(url_for('userBP.groupView'))

        elif function == 'new':
            form = groupForm()
            form.groupUsers.choices = [(str(r['id']),r['email']) for r in getUsers()['users']]

            if form.validate_on_submit():
                dataDict = {'name':form.groupName.data,
                            'desc':form.groupDesc.data,
                            'users':[int(r) for r in form.groupUsers.data]}
                newGroup = postGroup(dataDict)
                if 'error' in newGroup:
                    apiMessage(newGroup)
                else:
                    apiMessage(newGroup)
                    return redirect(url_for('userBP.groupView'))
        return render_template('user/groupForm.html', form=form)
