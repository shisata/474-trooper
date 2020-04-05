from blueprints import app
from flask import render_template, redirect, url_for, request, flash, session
from flask_mysqldb import MySQL
from datetime import date
import MySQLdb.cursors
import string
import mysql.connector

cnx = mysql.connector.connect(user="tnpham", password="SFU_cmpt474_P", host="walkingbus1.c11ymny8q9ji.us-east-1.rds.amazonaws.com", port=3306, database='walkingbus1')

def check_empty(input):
    if not(input and input.strip()):
        return True
    return False

#create group
@app.route('/creategroup', methods=['GET', 'POST'])
def createGroup():
    output =''
    if request.method == 'POST' and 'grpname' in request.form:
        grpname = request.form['grpname']

        if check_empty(grpname):
            output = 'group name must not be empty!'
        else:
            cnx.ping(True)
            cursor = cnx.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT ID from Walking_Groups WHERE GroupName = %s;', [grpname])
            grp = cursor.fetchone()
            cursor.close()

            if grp:
                output = 'Group Name is used, please input a new group name.'
            else:
                grpdescription = request.form['grpdescription']
                current_date = date.today()
                end_date = date(2099,12,31)
                cnx.ping(True)
                cursor = cnx.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('INSERT INTO Walking_Groups (GroupName, EffectiveStartDate, EffectiveEndDate, GroupDescription) VALUES (%s, %s, %s, %s)', [grpname, current_date, end_date, grpdescription])
                cnx.commit()
                cursor.execute('SELECT ID from Walking_Groups WHERE GroupName = %s;', [grpname])
                grp_id = cursor.fetchone()

                cursor.execute('INSERT INTO Group_Memberships (UserID, GroupID, RoleID, EffectiveStartDate, EffectiveEndDate) VALUES (%s, %s, %s, %s, %s)', [session['id'], grp_id[0], 1, current_date, end_date])
                cnx.commit()
                success_msg = "group " + grpname + " is created successfully!"
                cursor.close()
                return redirect(url_for('grpAdd', msg=success_msg))

            return render_template('creategrp.html', msg=output)

    return render_template('creategrp.html', msg=output)