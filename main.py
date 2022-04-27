# SJSU CMPE 138 Fall 2021 TEAM12
'''
CMPE 138 Team 12 Project: Laboratory
This file is the main entry point to our Command Line Interface based database application.
'''
import os
import mysql.connector
import datetime

import test_subject as ts
import utils
import lab_associate as la
import principal_investigator as pi
import research_scientist as rs
import admin

import bcrypt
import getpass
import logging
import re

role_array = ["Principal Investigator", "Lab Associate", "Research Scientist", "Admin", "Test Subject"]

init_string = """Welcome to the Laboratory Database App! 
Please select from the following roles before proceeding to log in: 
1. Principal Investigator 
2. Lab Associate
3. Research Scientist
4. Admin
5. Test Subject\n"""

def main():
    
    logging.basicConfig(filename='../Log/db.log',format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S', level=logging.INFO)
    
    print("""Welcome to the Laboratory Database App!""")
    
    mydb = mysql.connector.connect(
       host="localhost",
       user="root",
       password=os.environ['dbpass'],
       database="Laboratory"
    )
    mydb.autocommit = True
    cursor = mydb.cursor(buffered=True)

    username = verify_login(cursor)
    
    choice = getUserRole(cursor,username)

    if choice == 1:
        pi.pi_handler(cursor,username)
    elif choice == 2:
        la.la_handler(cursor,username)
    elif choice == 3:
        rs.rs_handler(cursor, username)
    elif choice == 4:
        admin.admin_handler(cursor, username)
    elif choice == 5:
        ts.ts_handler(cursor, username)
    else:
        return

    cursor.close()
    mydb.close()
        
    
def verify_login(cursor):
    username = str(input("Please enter your username: "))
    
    #check for starting letter to determine id type(emp or test subject)
    #re is overkill but has built-in empty check
    query = "SELECT hashed_pass FROM "
    if re.match("^e[0-9]+",username,re.IGNORECASE):
        query += "employee WHERE emp_id = "
        pass
    elif re.match("^ts[0-9]+",username,re.IGNORECASE):
        query += "test_subject WHERE ts_id = "
    elif re.match("^a[0-9]+",username,re.IGNORECASE):
        query += "administrator where emp_id = "
    else:
        print("Invalid username. Please relaunch app and try again.")
        quit() 
    
    p = getpass.getpass()
    
    query += "'" + username + "'"
    res = utils.query_executor(cursor, query)
    
    if not res:
        print("Something went wrong with the login verification process. Please relaunch app and try again.")
        quit()

    hashed_pass = cursor.fetchone()
    if bcrypt.checkpw(p.encode('utf8'), hashed_pass[0].encode('utf8')):
        print("Password matched! You may proceed.")
        return username
    else:
        print("Password did not match. Please relaunch app and try again.")
        quit()

def getUserRole(cursor,username):
    if re.match("^ts[0-9]+",username,re.IGNORECASE):
        return 5
    elif re.match("^a[0-9]+",username,re.IGNORECASE):
        return 4
    else:
        query = """select rs_flag, pi_flag, la_flag
                from employee
                where emp_id = '%s'"""%(username)
    
    utils.query_executor(cursor,query)
    flags = cursor.fetchone()
    if flags == (1,0,0):
        return 3
    elif flags == (0,1,0):
        return 1
    elif flags == (0,0,1):
        return 2
    else:
        print("Invalid user role. Please relaunch app and try again.")
        quit()
   
if __name__ == "__main__":
    main()