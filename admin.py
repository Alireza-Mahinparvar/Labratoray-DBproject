import re
import mysql.connector
import utils
import bcrypt

'''
CMPE 138 Team 12 Project: Laboratory

This file contains functions that contain all actions that can be carried out by the databse administrator.

'''

def print_current_deparment_entries(cursor):
    print("Current Deparment entries:")
    queryDepartment = """ 
    SELECT `department`.`dept_id`,
        `department`.`dept_name`,
        `department`.`dept_head`,
        `department`.`start_date`
    FROM `laboratory`.`department`;
    """
    if utils.query_executor(cursor, queryDepartment):
        json_result, _ = utils.convert_result_to_json(cursor)
        utils.display_json(json_result)

def create_department(cursor,user):
    print_current_deparment_entries(cursor)
    dept_id = input("\nPlease enter department id: ")
    dept_name = input("\nPlease enter department name: ")
    dept_head = input("\nPlease enter department head id : ")
    start_date = input("\nPlease enter Start Date('YYYY-MM-DD'):")
    
    query =""" INSERT INTO `laboratory`.`department`
    (`dept_id`, `dept_name`, `dept_head`, `start_date`) VALUES 
    ('%s', '%s', '%s', '%s'); """ % (dept_id, dept_name, dept_head, start_date)
    if utils.query_executor(cursor, query):
        print("Successfully created Department")
        print_current_deparment_entries(cursor)
        return True
    print("Failed to create Department")
    return False


def print_current_employee_entries(cursor):
    print("Current employee entries:")
    queryDepartment = """ 
    SELECT `employee`.`emp_id`,
        `employee`.`emp_fname`,
        `employee`.`emp_lname`,
        `employee`.`security_level`,
        `employee`.`credential`,
        `employee`.`rs_flag`,
        `employee`.`pi_flag`,
        `employee`.`la_flag`,
        `employee`.`supervisor_id`,
        `employee`.`dept_id`
    FROM `laboratory`.`employee`;
    """
    if utils.query_executor(cursor, queryDepartment):
        json_result, _ = utils.convert_result_to_json(cursor)
        utils.display_json(json_result)

def create_employee(cursor, user):
    print_current_employee_entries(cursor)
    emp_id         = input("Please enter employee id:")
    emp_fname      = input("Please enter employee first name:")
    emp_lname      = input("Please enter employee last name:")
    security_level = int(input("Please enter employee's security level:") or '1')
    credential     = input("Please enter credential:")
    
    options = """Please assign employee's role:
        1. Research Scientists
        2. Principal Investigator
        3. Lab Associate
        """
    choice = int(input(options) or '3')
    if choice == 1:
        role_assigned = 1, 0, 0
    elif choice == 2:
        role_assigned = 0, 1, 0
    elif choice == 3:
        role_assigned = 0, 0, 1
    else:
        role_assigned = 0, 0, 1
    
    rs_flag, pi_flag, la_flag = role_assigned

    pw = "pass" + str(emp_id)
    hashed_pass = bcrypt.hashpw(pw.encode('utf8'),bcrypt.gensalt()).decode('utf8')

    supervisor_id = input("Please enter employee's supervisor id:") or 'null'
    if supervisor_id != 'null':
        supervisor_id = ("'" + supervisor_id + "'")
        
    dept_id = input("Please enter employee's department id:")
    
    query = """
    INSERT INTO `laboratory`.`employee`
    (`emp_id`,
    `emp_fname`,
    `emp_lname`,
    `security_level`,
    `credential`,
    `rs_flag`,
    `pi_flag`,
    `la_flag`,
    `hashed_pass`,
    `supervisor_id`,
    `dept_id`)
    VALUES (
    '%s',
    '%s',
    '%s',
    '%s',
    '%s',
    '%s',
    '%s',
    '%s',
    '%s',
     %s,
    '%s'
    );
    """ % (emp_id,
    emp_fname,
    emp_lname,
    security_level,
    credential,
    rs_flag,
    pi_flag,
    la_flag,
    hashed_pass,
    supervisor_id,
    dept_id)  
    if utils.query_executor(cursor, query):
        print("Successfully added employee")
        print_current_employee_entries(cursor)
        return True
    print("Failed to add employee")
    return False


def print_current_equipment_entries(cursor):
    print("Current equipment entries:")
    queryDepartment = """ 
    SELECT `equipment`.`equ_id`,
        `equipment`.`equ_name`,
        `equipment`.`maintained_by`
    FROM `laboratory`.`equipment`;
    """
    if utils.query_executor(cursor, queryDepartment):
        json_result, _ = utils.convert_result_to_json(cursor)
        utils.display_json(json_result)

def create_equipment(cursor, user):
    print_current_equipment_entries(cursor)
    equ_id = input("Please enter equipment id:")
    equ_name = input("Please enter equipment name:")
    maintained_by = input("Please enter maintained by employee's id:") or 'null'
    if maintained_by != 'null':
        maintained_by = ("'" + maintained_by + "'")

    query = "INSERT INTO equipment (`equ_id`, `equ_name`, `maintained_by`) VALUES ('%s', '%s', %s)" % (equ_id, equ_name, maintained_by)
    if utils.query_executor(cursor, query):
        print("Successfully created equipment")
        print_current_equipment_entries(cursor)
        return True
    print("Failed to create equipment")
    return False

# a custom query function where you execute whatever the admin gives you
def custom_query(cursor, user):
    query = input("Please enter query:").lower()
    if utils.query_executor(cursor, query):
        print("Successfully executed query")
        if "select" in cursor.statement:
            json_result, _ = utils.convert_result_to_json(cursor)
            utils.display_json(json_result)
        return True
    print("Failed to execute query")
    return False


def admin_handler(cursor,user):
    
    options_array = [("Create Department", create_department,),
                     ("Create Employee", create_employee),
                     ("Create Equipment", create_equipment),
                     ("Custom Query", custom_query),
                    ("Exit",)]
    options_string = "Please select from the following actions allowed for your role by entering the number for the action:\n"
    for ind, val in enumerate(options_array):
        options_string += str(ind+1) + ". " + val[0] + "\n"

    exit_string = """You have chosen to EXIT so the databse application will close now. Please relaunch the app if you want to continue."""
    choice = 0
    while(choice!=len(options_array)):
        choice = int(input(options_string))
        if choice < len(options_array) and choice > 0:
            options_array[choice-1][1](cursor,user)
        elif choice != len(options_array):
            print("Please enter a valid option.")
