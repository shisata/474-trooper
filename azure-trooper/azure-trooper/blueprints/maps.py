from blueprints import app
from flask import render_template, session, request, redirect, url_for
from datetime import date
from flask_mysqldb import MySQL
import MySQLdb.cursors
import mysql.connector

cnx = mysql.connector.connect(user="tnpham", password="SFU_cmpt474_P", host="walkingbus1.c11ymny8q9ji.us-east-1.rds.amazonaws.com", port=3306, database='walkingbus1')

#show map
@app.route('/map')
def showmap():
    cnx.ping(True)
    cursor = cnx.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT ID, GroupName from Walking_Groups;')
    result = cursor.fetchall()
    groups = []
    for grp in result:
        (id, grpname) = grp
        groups.append([id, grpname])
    cursor.close()
    print(groups)
    return render_template('maps.html', groups=groups)

@app.route('/group/<int:id>', methods=['GET'])
def showgrp(id):
    success_msg = request.args.get('success', default='')
    error_msg = request.args.get('error', default='')

    cnx.ping(True)
    cursor = cnx.cursor(MySQLdb.cursors.DictCursor)
    # get group details
    cursor.execute('SELECT ID, GroupName, GroupDescription from Walking_Groups where ID = %s;', [id])
    result = cursor.fetchone()
    (ID, GroupName, GroupDescription) = result
    grp_detail= [ID, GroupName, GroupDescription]

    # get member list
    cursor.execute('SELECT gr.RoleName, u.Email, ut.TypeName from Group_Memberships gm join Group_Roles gr on gm.RoleID = gr.ID join Users u on gm.UserID = u.ID join User_Types ut on u.UserTypeID = ut.ID where gm.GroupID = %s;', [id])
    result = cursor.fetchall()
    members = []
    for grp in result:
        (RoleName, Email, TypeName) = grp
        members.append([Email, TypeName, RoleName])

    #check if user is a member of the group
    cursor.execute('SELECT RoleID from Group_Memberships where GroupID = %s and UserID = %s;', [id, session['id']])
    flag = cursor.fetchone()
    cursor.close()

    isMember = 0
    isOwner = 0
    if flag:
        #check if user is group owner
        if flag[0] == 1:
            isOwner = 1
        else:
            isMember = 1    
    return render_template('grouppg.html', grp_detail=grp_detail, members=members, isOwner=isOwner, isMember=isMember, success_msg=success_msg, error_msg=error_msg)

@app.route('/joingrp/<int:id>', methods=['GET'])
def joingrp(id):
    current_date = date.today()
    end_date = date(2099,12,31)
    cnx.ping(True)
    cursor = cnx.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('INSERT INTO Group_Memberships (UserID, GroupID, RoleID, EffectiveStartDate, EffectiveEndDate) values (%s, %s, %s, %s, %s);', [session['id'], id, 2, current_date, end_date])
    cnx.commit()
    cursor.close()
    success_msg = "you have joined group - " + str(id) + " successfully!"
    return redirect(url_for('grpJoin', msg=success_msg, id=id))
    

