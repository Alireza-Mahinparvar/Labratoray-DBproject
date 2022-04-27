# SJSU CMPE 138 Fall 2021 TEAM12
'''
CMPE 138 Team 12 Project: Laboratory
This file contains fucntions that implemenent a Principal Investigator's functionalities/operations.
'''

import utils
from utils import convert_result_to_json, query_executor, display_json

operation_string = '''
Please enter the name of the operation you would like to perform from the following options:
1. create
2. update
3. approve
4. view
5. EXIT
'''


entity_string = '''
Please enter the name of the entity on which you would like to perform the operation:
a. project
b. experiment
c. trial
d. publication
e. work_assignment
f. equipment_allocation
'''

operation_dict = {
    '1': 'create_',
    '2': 'update_',
    '3': 'approve_',
    '4': 'view_',
    '5': 'exit'
}

entity_dict = {
    'a': 'project',
    'b': 'experiment',
    'c': 'trial',
    'd': 'publication',
    'e': 'work_assignment',
    'f': 'equipment_allocation'
}

def pi_handler(cursor, username):
     
    outer_choice = 0
    
    while (outer_choice != 5):
        outer_choice = input(operation_string)
        
        if outer_choice == '5':
            exit_string = """You have chosen to EXIT so the databse application will close now. Please relaunch the app if you want to continue."""
            return
            
        if outer_choice not in ('1','2','3','4','5'):
            print("Please enter a valid number and try again.")
            continue
            
        operation = operation_dict[outer_choice]
        
        inner_choice = input(entity_string)
        
        if inner_choice not in ('a', 'b', 'c', 'd', 'e', 'f'):
            print("Invalid choice. Please try again.")
            continue
            
        entity = entity_dict[inner_choice]
        
        func_name = operation + entity 
        try:
            globals()[func_name](cursor, username)
        except error:
            print("Invalid choice. Please relaunch app again.")
            quit()
        
        
def create_project(cursor, username):

    query1 = "SELECT dept_id FROM employee where emp_id = %s"
    if not utils.query_executor(cursor, query1, (username,)):
        return
        
    result = cursor.fetchone()
    dept_id = str(result[0])
    
    print("\nThese are the current projects in your department:\n")
    query2 = "SELECT * FROM project WHERE dept_id = %s"
    if not utils.query_executor(cursor, query2, (dept_id,)):
        return
    
    json_result, result = utils.convert_result_to_json(cursor)
    utils.display_json(json_result)
    
    count_fetch = "SELECT pro_id FROM project ORDER BY pro_id desc"
    if not utils.query_executor(cursor, count_fetch):
        return
    
    result = cursor.fetchall()    
    if cursor.rowcount < 1:
        next_pro_id = 1
    else:
        next_pro_id = int(result[0][0]) + 1
    
    
    print("\nPlease provide values for the project you want to create and sign up to be PI for:")
    pro_name = input("Project Name: ")
    pro_status = 'Planned'
    proj_leader = username

    query3 = ("INSERT INTO project "
             "(pro_id, pro_name, pro_status, dept_id, proj_leader) "
             "VALUES (%s, %s, %s, %s, %s)")
    
    if not utils.query_executor(cursor, query3, (next_pro_id, pro_name, pro_status, dept_id, proj_leader)):
        return        
    
    print("\nThe following project was successfully added to the database!")
    
    query4 = "SELECT * FROM project WHERE pro_id = %s"
    if not utils.query_executor(cursor, query4, (next_pro_id,)):
        return
        
    json_result, result = utils.convert_result_to_json(cursor)
    utils.display_json(json_result)

    
def create_experiment(cursor, username):
    query1 = "SELECT dept_id FROM employee where emp_id = %s"
    if not utils.query_executor(cursor, query1, (username,)):
        return
        
    result = cursor.fetchone()
    dept_id = str(result[0])
    
    print("\nThese are the current projects in your department that are still ongoing or Planned:\n")
    query2 = "SELECT * FROM project WHERE dept_id = %s AND (pro_status = 'ongoing' OR pro_status = 'Planned')"
    if not utils.query_executor(cursor, query2, (dept_id,)):
        return
    
    json_result, result = utils.convert_result_to_json(cursor)
    utils.display_json(json_result)
    
    pro_id = input("Please enter the id of the project to which you would like to add an experiment: ") 
    
    print("\nFollowing are the experiments under the project you have selected:")
    query3 = "SELECT * FROM experiment WHERE pro_id = %s and trial_flag = 0"
    if not utils.query_executor(cursor, query3, (pro_id,)):
        return
        
    json_result, result = utils.convert_result_to_json(cursor)
    utils.display_json(json_result)
    
    count_fetch = "SELECT exp_id FROM experiment ORDER BY exp_id desc"
    if not utils.query_executor(cursor, count_fetch):
        return
    
    result = cursor.fetchall()    
    if cursor.rowcount < 1:
        next_exp_id = 1
    else:
        next_exp_id = int(result[0][0]) + 1
    
    print("\nPlease provide values for the experiment you would like to create:")
    exp_name = input("Experiment Name: ")
    exp_status = 'Planned'
    trial_flag = 0
    
    query4 = ("INSERT INTO experiment "
             "(exp_id, exp_name, exp_status, pro_id, trial_flag) "
             "VALUES (%s, %s, %s, %s, %s)")
             
    if not utils.query_executor(cursor, query4, (next_exp_id, exp_name, exp_status, pro_id, trial_flag)):
        return
        
    print("\nThe following experiment was successfully added to the database!")
    
    query5 = "SELECT * FROM experiment WHERE exp_id = %s"
    if not utils.query_executor(cursor, query5, (next_exp_id,)):
        return
        
    json_result, result = utils.convert_result_to_json(cursor)
    utils.display_json(json_result)        
    
    
    
def create_trial(cursor, username):
    query1 = "SELECT dept_id FROM employee where emp_id = %s"
    if not utils.query_executor(cursor, query1, (username,)):
        return
        
    result = cursor.fetchone()
    dept_id = str(result[0])
    
    print("\nThese are the current projects in your department that are still ongoing or Planned:\n")
    query2 = "SELECT * FROM project WHERE dept_id = %s AND (pro_status = 'ongoing' OR pro_status = 'Planned')"
    if not utils.query_executor(cursor, query2, (dept_id,)):
        return
    
    json_result, result = utils.convert_result_to_json(cursor)
    utils.display_json(json_result)
    
    pro_id = input("Please enter the id of the project to which you would like to add a trial: ") 
    
    print("\nFollowing are the trials under the project you have selected:")
    query3 = "SELECT * FROM experiment WHERE pro_id = %s and trial_flag = 1"
    if not utils.query_executor(cursor, query3, (pro_id,)):
        return
        
    json_result, result = utils.convert_result_to_json(cursor)
    utils.display_json(json_result)
    
    count_fetch = "SELECT exp_id FROM experiment ORDER BY exp_id desc"
    if not utils.query_executor(cursor, count_fetch):
        return
    
    result = cursor.fetchall()    
    if cursor.rowcount < 1:
        next_exp_id = 1
    else:
        next_exp_id = int(result[0][0]) + 1
    
    print("\nPlease provide values for the trial you would like to create:")
    exp_name = input("Trial Name: ")
    exp_status = 'Planned'
    trial_flag = 1
    criteria = input("Description of the trial criteria: ")
    agerange_start = input("Start age of trial eligibility: ")
    agerange_end = input("End age of trial eligibility: ")
    gender = input("Allowed genders (F, M or A for all): ")
    num_allowed_participants = input("Number of allowed participants: ")
    
    
    query4 = ("INSERT INTO experiment "
             "(exp_id, exp_name, exp_status, pro_id, trial_flag) "
             "VALUES (%s, %s, %s, %s, %s)")
             
    if not utils.query_executor(cursor, query4, (next_exp_id, exp_name, exp_status, pro_id, trial_flag)):
        return
        
    query5 = ("INSERT INTO trial "
             "(exp_id, criteria, agerange_start, agerange_end, gender, num_allowed_participants) "
             "VALUES (%s, %s, %s, %s, %s, %s)")
    if not utils.query_executor(cursor, query5, (next_exp_id, criteria, agerange_start, agerange_end, gender, num_allowed_participants)):
        return         
        
    print("\nThe following trial was successfully added to the database!")
    
    query5 = ("SELECT experiment.exp_id, exp_name, exp_status, criteria, agerange_start, agerange_end, "
             "gender, num_allowed_participants FROM experiment JOIN trial ON (experiment.exp_id = trial.exp_id) "
             "WHERE experiment.exp_id = %s")
             
    if not utils.query_executor(cursor, query5, (next_exp_id,)):
        return
        
    json_result, result = utils.convert_result_to_json(cursor)
    utils.display_json(json_result)
    

def create_publication(cursor, username):
    query1 = "SELECT dept_id FROM employee where emp_id = %s"
    if not utils.query_executor(cursor, query1, (username,)):
        return
        
    result = cursor.fetchone()
    dept_id = str(result[0])
    
    print("\nThese are the current projects in your department that are still ongoing or Planned:\n")
    query2 = "SELECT * FROM project WHERE dept_id = %s AND (pro_status = 'ongoing' OR pro_status = 'Planned')"
    if not utils.query_executor(cursor, query2, (dept_id,)):
        return
    
    json_result, result = utils.convert_result_to_json(cursor)
    utils.display_json(json_result)
    
    pro_id = input("Please enter the id of the project to which you would like to add a trial: ") 
    
    print("\nFollowing are the publications under the project you have selected:")
    query3 = "SELECT * FROM publication WHERE pro_id = %s"
    if not utils.query_executor(cursor, query3, (pro_id,)):
        return
        
    json_result, result = utils.convert_result_to_json(cursor)
    utils.display_json(json_result)
    
    count_fetch = "SELECT pub_id FROM publication ORDER BY pub_id desc"
    if not utils.query_executor(cursor, count_fetch):
        return
    
    result = cursor.fetchall()    
    if cursor.rowcount < 1:
        next_pub_id = 1
    else:
        next_pub_id = int(result[0][0]) + 1
        
    print("\nPlease provide values for the publication you would like to create:")
    pub_name = input("Publication name: ")
    pub_status = 'Planned'
    journal = input("Journal: ")
    
    query4 = ("INSERT INTO publication "
             "(pub_id, pub_name, pub_status, pro_id, journal) "
             "VALUES (%s, %s, %s, %s, %s)")
             
    if not utils.query_executor(cursor, query4, (next_pub_id, pub_name, pub_status, pro_id, journal)):
        return
    
    print("\nThe following publication was successfully added to the database!")
    
    query5 = "SELECT * FROM publication WHERE pub_id = %s"
    if not utils.query_executor(cursor, query5, (next_pub_id,)):
        return
        
    json_result, result = utils.convert_result_to_json(cursor)
    utils.display_json(json_result)
    
    
def create_work_assignment(cursor, username):
    query1 = "SELECT dept_id FROM employee where emp_id = %s"
    if not utils.query_executor(cursor, query1, (username,)):
        return
        
    result = cursor.fetchone()
    dept_id = str(result[0])
    
    print("\nThese are the current projects in your department that are still ongoing or Planned:\n")
    query2 = "SELECT * FROM project WHERE dept_id = %s AND (pro_status = 'ongoing' OR pro_status = 'Planned')"
    if not utils.query_executor(cursor, query2, (dept_id,)):
        return
    
    json_result, result = utils.convert_result_to_json(cursor)
    utils.display_json(json_result)
    
    pro_id = input("Please enter the id of the project to which you like to assign a Research Scientist to work on: ")
    
    query3 = "SELECT emp_id, emp_fname, emp_lname FROM employee WHERE dept_id = %s AND rs_flag = 1"
    if not utils.query_executor(cursor, query3, (dept_id,)):
        return
        
    print("\nFollowing are the research scientists currently in your department: ")
    json_result, result = utils.convert_result_to_json(cursor)
    utils.display_json(json_result)
    
    emp_id = input("Please enter the employee ID of the research scientist you would like to"
                   " assign to the project chosen above: ")
                   
    check_query = "SELECT * FROM works_on WHERE pro_id=%s AND emp_id=%s"
    if not utils.query_executor(cursor, check_query, (pro_id, emp_id)):
        return
        
    result = cursor.fetchall()
    if cursor.rowcount > 0:
        print("This work assignment already exists.\n")
        return
    
    query4 = ("INSERT INTO works_on "
             "(emp_id, pro_id) "
             "VALUES (%s, %s)")
             
    if not utils.query_executor(cursor, query4, (emp_id, pro_id)):
        return
        
    query5 = "SELECT * FROM works_on WHERE emp_id = %s AND pro_id = %s"
    
    if not utils.query_executor(cursor, query5, (emp_id, pro_id)):
        return
        
    print("\nFollowing work assignment was added to the database! ")
    json_result, result = utils.convert_result_to_json(cursor)
    utils.display_json(json_result)
    
    
    
def update_project(cursor, username):
    query1 = "SELECT dept_id FROM employee where emp_id = %s"
    if not utils.query_executor(cursor, query1, (username,)):
        return
        
    result = cursor.fetchone()
    dept_id = str(result[0])
    
    print("\nFollowing are the projects in your department:\n")
    query2 = "SELECT * FROM project WHERE dept_id = %s"
    if not utils.query_executor(cursor, query2, (dept_id,)):
        return
    
    json_result, result = utils.convert_result_to_json(cursor)
    utils.display_json(json_result)
    
    pro_id = input("Please enter the id of the project you would like to update: ")
    query3 = "SELECT * FROM project WHERE pro_id = %s"
    if not utils.query_executor(cursor, query3, (pro_id,)):
        return
    col_names = [i[0] for i in cursor.description]
    
    print("\n This is the current state of the project you are trying to update:")
    json_result, result = utils.convert_result_to_json(cursor)
    utils.display_json(json_result)
    
    field_name = ''
    fields = {}
    
    while field_name != 'stop':
        field_name = input("Please enter the name of the field you would like to update (enter stop when done): ")
        
        if field_name == 'stop':
            break
        
        if field_name not in col_names:
            print("Invalid field name. Please try again.")
            continue
        
        field_value = input("Please enter a value for the field you would like to update: ")
        
        fields[field_name] = field_value
        
    query4 = "UPDATE project SET "
    
    values = []
    for key in fields:
        temp_str = f"{key} = %s, "
        query4 += temp_str
        values.append(fields[key])
     
    values.append(pro_id)   
    vals = tuple(values)
    
    query5 = query4[:len(query4)-2] + " WHERE pro_id = %s"
    if not utils.query_executor(cursor, query5, vals):
        return
        
    print("The project you requested was successfully updated in the database!\n")
    query6 = "SELECT * FROM project WHERE pro_id = %s"
    
    if not utils.query_executor(cursor, query6, (pro_id,)):
        return
    
    json_result, result = utils.convert_result_to_json(cursor)
    utils.display_json(json_result)
    
    
def update_experiment(cursor, username):
    query1 = "SELECT dept_id FROM employee where emp_id = %s"
    if not utils.query_executor(cursor, query1, (username,)):
        return
        
    result = cursor.fetchone()
    dept_id = str(result[0])
    
    print("\nFollowing are the experiments in your department:\n")
    query2 = ("SELECT experiment.exp_id, experiment.exp_name FROM experiment JOIN project "
             "ON experiment.pro_id = project.pro_id WHERE project.dept_id = %s AND experiment.trial_flag = 0")
    if not utils.query_executor(cursor, query2, (dept_id,)):
        return
    
    if cursor.rowcount < 1:
        print("There are no experiments currently in your department, hence there is nothing to update.")
        return
    
    json_result, result = utils.convert_result_to_json(cursor)
    utils.display_json(json_result)
    
    exp_id = input("Please enter the id of the experiment you would like to update: ")
    query3 = "SELECT * FROM experiment WHERE exp_id = %s"
    if not utils.query_executor(cursor, query3, (exp_id,)):
        return
    col_names = [i[0] for i in cursor.description]
    
    print("\n This is the current state of the project you are trying to update:")
    json_result, result = utils.convert_result_to_json(cursor)
    utils.display_json(json_result)
    
    field_name = ''
    fields = {}
    
    while field_name != 'stop':
        field_name = input("Please enter the name of the field you would like to update (enter stop when done): ")
        
        if field_name == 'stop':
            break
        
        if field_name not in col_names:
            print("Invalid field name. Please try again.")
            continue
        
        field_value = input("Please enter a value for the field you would like to update: ")
        
        fields[field_name] = field_value
        
    query4 = "UPDATE experiment SET "
    
    values = []
    for key in fields:
        temp_str = f"{key} = %s, "
        query4 += temp_str
        values.append(fields[key])
     
    values.append(exp_id)   
    vals = tuple(values)
    
    query5 = query4[:len(query4)-2] + " WHERE exp_id = %s"
    if not utils.query_executor(cursor, query5, vals):
        return
        
    print("The experiment you requested was successfully updated in the database!\n")
    query6 = "SELECT * FROM experiment WHERE exp_id = %s"
    
    if not utils.query_executor(cursor, query6, (exp_id,)):
        return
    
    json_result, result = utils.convert_result_to_json(cursor)
    utils.display_json(json_result)
    
    
def update_trial(cursor, username):
    query1 = "SELECT dept_id FROM employee where emp_id = %s"
    if not utils.query_executor(cursor, query1, (username,)):
        return
        
    result = cursor.fetchone()
    dept_id = str(result[0])
    
    print("\nFollowing are the trials in your department:\n")
    query2 = ("SELECT experiment.exp_id, experiment.exp_name FROM experiment JOIN project "
             "ON experiment.pro_id = project.pro_id WHERE project.dept_id = %s AND experiment.trial_flag = 1")
    if not utils.query_executor(cursor, query2, (dept_id,)):
        return
    
    if cursor.rowcount < 1:
        print("There are no trials currently in your department, hence there is nothing to update.")
        return
    
    json_result, result = utils.convert_result_to_json(cursor)
    utils.display_json(json_result)
    
    exp_id = input("Please enter the id of the trial you would like to update: ")
    query3 = "SELECT * FROM experiment WHERE exp_id = %s"
    if not utils.query_executor(cursor, query3, (exp_id,)):
        return
    
    col_names_exp = [i[0] for i in cursor.description]
    
    query4 = "SELECT * FROM trial WHERE exp_id = %s"
    if not utils.query_executor(cursor, query4, (exp_id,)):
        return
    
    col_names_trial = [i[0] for i in cursor.description]
    
    print("1.", col_names_exp)
    print("2.", col_names_trial)
    choice = input("\nWould like to update fields from List 1 or List 2? ")
    
    if choice == '1':
        update_trial_exp(cursor, username, exp_id, col_names_exp)
    elif choice == '2':
        update_trial_trial(cursor, username, exp_id, col_names_trial)
    
    
def update_trial_exp(cursor, username, exp_id, col_names):
    print("\nThis is the current state of the trial you are trying to update:")
    
    query3 = "SELECT * FROM experiment WHERE exp_id = %s"
    if not utils.query_executor(cursor, query3, (exp_id,)):
        return
        
    json_result, result = utils.convert_result_to_json(cursor)
    utils.display_json(json_result)
    
    field_name = ''
    fields = {}
    
    while field_name != 'stop':
        field_name = input("Please enter the name of the field you would like to update (enter stop when done): ")
        
        if field_name == 'stop':
            break
        
        if field_name not in col_names:
            print("Invalid field name. Please try again.")
            continue
        
        field_value = input("Please enter a value for the field you would like to update: ")
        
        fields[field_name] = field_value
        
    query4 = "UPDATE experiment SET "
    
    values = []
    for key in fields:
        temp_str = f"{key} = %s, "
        query4 += temp_str
        values.append(fields[key])
     
    values.append(exp_id)   
    vals = tuple(values)
    
    query5 = query4[:len(query4)-2] + " WHERE exp_id = %s"
    if not utils.query_executor(cursor, query5, vals):
        return
        
    print("The trial you requested was successfully updated in the database!\n")
    query6 = "SELECT * FROM experiment WHERE exp_id = %s"
    
    if not utils.query_executor(cursor, query6, (exp_id,)):
        return
    
    json_result, result = utils.convert_result_to_json(cursor)
    utils.display_json(json_result)
    
    
def update_trial_trial(cursor, username, exp_id, col_names):
    print("\nThis is the current state of the trial you are trying to update:")
    
    query3 = "SELECT * FROM trial WHERE exp_id = %s"
    if not utils.query_executor(cursor, query3, (exp_id,)):
        return
        
    json_result, result = utils.convert_result_to_json(cursor)
    utils.display_json(json_result)
    
    field_name = ''
    fields = {}
    
    while field_name != 'stop':
        field_name = input("Please enter the name of the field you would like to update (enter stop when done): ")
        
        if field_name == 'stop':
            break
        
        if field_name not in col_names:
            print("Invalid field name. Please try again.")
            continue
        
        field_value = input("Please enter a value for the field you would like to update: ")
        
        fields[field_name] = field_value
        
    query4 = "UPDATE trial SET "
    
    values = []
    for key in fields:
        temp_str = f"{key} = %s, "
        query4 += temp_str
        values.append(fields[key])
     
    values.append(exp_id)   
    vals = tuple(values)
    
    query5 = query4[:len(query4)-2] + " WHERE exp_id = %s"
    if not utils.query_executor(cursor, query5, vals):
        return
        
    print("The trial you requested was successfully updated in the database!\n")
    query6 = "SELECT * FROM trial WHERE exp_id = %s"
    
    if not utils.query_executor(cursor, query6, (exp_id,)):
        return
    
    json_result, result = utils.convert_result_to_json(cursor)
    utils.display_json(json_result)
    
    

def update_publication(cursor, username):
    query1 = "SELECT dept_id FROM employee where emp_id = %s"
    if not utils.query_executor(cursor, query1, (username,)):
        return
        
    result = cursor.fetchone()
    dept_id = str(result[0])
    
    print("\nFollowing are the publications in your department:\n")
    query2 = ("SELECT publication.pub_id, publication.pub_name FROM publication JOIN project "
             "ON publication.pro_id = project.pro_id WHERE project.dept_id = %s")
    if not utils.query_executor(cursor, query2, (dept_id,)):
        return
    
    if cursor.rowcount < 1:
        print("There are no experiments currently in your department, hence there is nothing to update.")
        return
    
    json_result, result = utils.convert_result_to_json(cursor)
    utils.display_json(json_result)
    
    pub_id = input("Please enter the id of the publication you would like to update: ")
    query3 = "SELECT * FROM publication WHERE pub_id = %s"
    if not utils.query_executor(cursor, query3, (pub_id,)):
        return
    col_names = [i[0] for i in cursor.description]
    
    print("\n This is the current state of the publication you are trying to update:")
    json_result, result = utils.convert_result_to_json(cursor)
    utils.display_json(json_result)
    
    field_name = ''
    fields = {}
    
    while field_name != 'stop':
        field_name = input("Please enter the name of the field you would like to update (enter stop when done): ")
        
        if field_name == 'stop':
            break
        
        if field_name not in col_names:
            print("Invalid field name. Please try again.")
            continue
        
        field_value = input("Please enter a value for the field you would like to update: ")
        
        fields[field_name] = field_value
        
    query4 = "UPDATE publication SET "
    
    values = []
    for key in fields:
        temp_str = f"{key} = %s, "
        query4 += temp_str
        values.append(fields[key])
     
    values.append(pub_id)   
    vals = tuple(values)
    
    query5 = query4[:len(query4)-2] + " WHERE pub_id = %s"
    if not utils.query_executor(cursor, query5, vals):
        return
        
    print("The publication you requested was successfully updated in the database!\n")
    query6 = "SELECT * FROM publication WHERE pub_id = %s"
    
    if not utils.query_executor(cursor, query6, (pub_id,)):
        return
    
    json_result, result = utils.convert_result_to_json(cursor)
    utils.display_json(json_result)
    
def approve_publication(cursor,username):
    _input1 = str(input("\nPlease enter publication id : "))
    _input2 = str(input("\nPlease enter publication approval date : "))
    query1="UPDATE publication SET approved_by = '%s',approved_date='%s', pub_status='done' WHERE pub_id='%s'" %(username,_input2,_input1)
    if not utils.query_executor(cursor, query1):
        return
        
def approve_trial():
    approve_experiment()

def approve_experiment(cursor, username):
    """ Allows the Principal Investigator to aprove a specified experiment
    from the experiment table"""

    # Get experiment id
    # emp_id = str(input("Please enter your employee id number: "))
    # Verify that the employee id is valid
    print("Here is the list of current experiments")
    # view the table of experiments
    view_table(cursor, experiment=True)
    exp_id = str(input("\nPlease type the experiment/trial ID you would like to approve: "))
    if not verify_username(cursor, username, exp_id):
        return
    emp_id = username
    # Calls query to approve experiment
    query = ("UPDATE EXPERIMENT\
        SET exp_status =%s\
        WHERE exp_id =%s\
            AND approved_by=%s")
    data = ('Done', exp_id, emp_id)
    query_executor(cursor, query, data)
    cursor.execute(query, data)

    print("\nThank you, the experiment has been approved\n")
    # Prints table showing approved experiment
    view_table(cursor, experiment=True)
    return
    
def view_project(cursor, username):
    view_table(cursor, username, project=True)
    
def view_experiment(cursor, username):
    view_table(cursor, username, experiment=True)
    
def view_trial(cursor, username):
    view_table(cursor, username, experiment=True)
    
def view_publication(cursor, username):
    view_table(cursor, username, publication=True)

def view_table(cursor, username, employee=False, project=False, experiment=False, publication=False):
    """Displays the relevant table views for the principal investigator.
    Currently is set to only be called from other functions.
    Can view employee table, project table and experiment table"""

    if not employee and not project and not experiment and not publication:
        print("Please select a table to view")
        table = str(input("Employee (1), Project (2), Experiment (3), Publication (4): "))
        if table == "1":
            employee = True
        elif table == "2":
            project = True
        elif table == "3":
            experiment = True
        elif table == '4':
            publication = True
        else:
            print("Please enter a valid number")
            return

    if employee:
        print("\nHere is the list of employees in db\n")
        query = ("SELECT emp_id, emp_fname as F_Name, emp_lname as L_Name\
            FROM employee")
        query_executor(cursor, query)
        json_result, result_set = convert_result_to_json(cursor)
        if len(result_set)==0:
            print("No results found\n")
            return
        display_json(json_result)

    if project:
        print("\nHere is the list of projects in db\n")
        query = ("SELECT pro_id as Project_Id, pro_name as Project_Name, pro_sdate as Start_Date, pro_edate as End_Date, pro_status\
            FROM project")
        query_executor(cursor, query)
        query_executor(cursor, query)
        json_result, result_set = convert_result_to_json(cursor)
        if len(result_set)==0:
            print("No results found\n")
            return
        display_json(json_result)
    if experiment:
        print("\nHere is the list of experiments and trials in db\n")
        query = ("SELECT exp_id, exp_name, trial_flag, exp_sdate as Start_Date, exp_edate as End_Date, exp_status as Status, pro_id\
            FROM experiment")
        query_executor(cursor, query)
        json_result, result_set = convert_result_to_json(cursor)
        if len(result_set)==0:
            print("No results found\n")
            return
        display_json(json_result)
    if publication:
        print("\nHere is the list of publication in db\n")
        query = ("SELECT pub_id, pub_name, pub_status, pro_id\
            FROM publication")
        query_executor(cursor, query)
        json_result, result_set = convert_result_to_json(cursor)
        if len(result_set)==0:
            print("No results found\n")
            return
        display_json(json_result)

    return

def view_work_assignment(cursor, username):
    """ Allows the principal investigator to view the current work allocation
    for each research scientist. """

    print("Here is the current work allocation for your Research Scientists")
    query = ("SELECT e.emp_fname as F_Name, e.emp_lname as L_Name, p.pro_name as Project_Name, p.pro_sdate as Start_Date,\
         p.pro_edate as End_Date, p.pro_status as Project_Status, p.dept_id\
    FROM project p INNER JOIN works_on w ON p.pro_id = w.pro_id\
    INNER JOIN employee e ON w.emp_id = e.emp_id""")
    query_executor(cursor, query)
    query_executor(cursor, query)
    json_result, result_set = convert_result_to_json(cursor)
    if len(result_set)==0:
        print("No results found\n")
        return
    display_json(json_result)

    return

def view_equipment_allocation(cursor, username):
    """ Allows the principal investigator to view the current equipment allocation
    for each employee. This function can be called from either pi_handler or called
    from within another function in this file."""

    print("\nHere is the current equipment allocation\n")
    # Create and execute query
    query = ("SELECT equipment.equ_id, equipment.equ_name, emp_fname as F_Name, emp_lname as L_Name\
        FROM equipment INNER JOIN employee ON\
            equipment.maintained_by = employee.emp_id")
    # Execute query
    query_executor(cursor, query)
    # Get result set
    query_executor(cursor, query)
    json_result, result_set = convert_result_to_json(cursor)
    if len(result_set)==0:
        print("No results found\n")
        return
    display_json(json_result)
    return

def create_equipment_allocation(cursor, username):
    """ Queries the principal investigator for an equipment name and assignee id,
    then generates an equipment id and inserts equipment with updated employee assignment
    into db"""
    # Prints the current equipment allocation
    # view_equipment_allocation(cursor)
    print("\nHere is the list of current equipment")
    # view the table of equipment
    query = ("SELECT equ_id, equ_name, maintained_by\
        FROM equipment")
    query_executor(cursor, query)
    query_executor(cursor, query)
    json_result, result_set = convert_result_to_json(cursor)
    if len(result_set)==0:
        print("No results found\n")
        return
    display_json(json_result)

    # Prints the current employee set in table
    view_table(cursor, username, employee=True)
    # Queries user for new equipment name
    equipment_id = str(input("\nPlease enter the id of the equipment you would like to assign: "))
    # Queries user for the employee id of whom to assign it to
    assignee_id = str(input("\nPlease enter the employee id of whom you'd like to assign the equipment to: "))
    # Check if employee in db
    if not check_employee_in_db_helper(cursor, assignee_id):
        return
    # Check if equipment in db
    if not check_equipment_in_db_helper(cursor, equipment_id):
        return
    # Assigns equipment to employee given that employee is in db
    query = ("UPDATE equipment SET maintained_by = %s WHERE equ_id = %s")
    vals = (assignee_id, equipment_id)
    # Execute query
    query_executor(cursor, query, vals)
    # Prints the current equipment allocation
    print("\nThank you, the equipment has been assigned\n")
    # Prints the current equipment allocation
    view_equipment_allocation(cursor, username)
    print("\n")

    return

def update_equipment_allocation(cursor, username):
    """ Allows the principal investigator to update equipment assignment for a given equipment
    name. First displays the current list of equipment and employees. Then asks the PI to input the
    employee id and equipment id for which the equipment assignment will be updated to. """

    # Prints the current equipment allocation
    print("Here is a list of the current equipment assignments in the database: ")
    # Print list of employees and equipment
    query = ("""SELECT equipment.equ_id, equipment.equ_name, employee.emp_fname as F_Name, employee.emp_lname as L_Name\
        FROM equipment INNER JOIN employee ON\
            equipment.maintained_by = employee.emp_id""")
    query_executor(cursor, query)
    json_result, result_set = convert_result_to_json(cursor)
    if len(result_set)==0:
        print("No results found\n")
        return
    display_json(json_result)
    # Display the employee table
    view_table(cursor, username, employee=True)
    # Ask for equipment id and employee id
    equ_id = str(input("\nPlease enter the equipment id you would like to update: "))
    # Check if equipment is in database
    if not check_equipment_helper(cursor, equ_id):
        return
    # Get the employee id for whom the equipment will be updated to
    emp_id = str(input("\nPlease enter the employee id of the person \
you would like to update equipment assignment to: "))
    # Check if employee is in db
    if not check_employee_in_db_helper(cursor, emp_id):
        return
    # Assigns equipment to employee given that employee is in db
    query = ("UPDATE equipment\
    SET maintained_by= %s\
    WHERE equ_id = %s""")
    data = (emp_id, equ_id)
    # Execute query
    query_executor(cursor, query, data)
    print("Thank you, the equipment assignment has been updated, the new equipment assignment is: ")
    # Views current equipment allocation for pi to confirm update is correct
    view_equipment_allocation(cursor, username)
    print("\n")
    return

def check_employee_in_db_helper(cursor, emp_id):
    """ Helper function to check whether selected employee is in db"""

    query = ("SELECT emp_fname as F_Name FROM employee\
        WHERE emp_id =%s")
    data = (emp_id,)
    # Execute query
    query_executor(cursor, query, data)
    if cursor.rowcount == 0:
        # If no results are found
        print("\nSorry, the employee you would like to assign equipment to is not in the database\n")
        return False
    # If results are found
    return True

def check_equipment_helper(cursor, equ_id):
    """ Helper function to check whether selected equipment is in db"""
    query = ("SELECT equ_id FROM equipment WHERE equ_id =%s")
    data = (equ_id,)
    # Execute query
    query_executor(cursor, query, data)
    if cursor.rowcount == 0:
        # If equipment is not in db
        print("\nSorry, the equipment you would like to assign to is not in the database\n")
        return False
    # If equipment is in db
    return True

def check_exp_id_helper(cursor, exp_id):
    """ Helper function to check whether selected experiment is in db"""
    query = ("SELECT exp_id FROM experiment WHERE exp_id =%s")
    data = (exp_id,)
    # Execute query
    query_executor(cursor, query, data)
    if cursor.rowcount == 0:
        # If no results are found, print message
        print("\nSorry, the experiment you would like to assign to is not in the database\n")
        return False
    # If results are found
    return True

def check_equipment_in_db_helper(cursor, equipment_id):
    """ Helper function to check whether selected equipment is in db"""
    query = ("SELECT equ_id FROM equipment WHERE equ_id =%s")
    data = (equipment_id,)
    # Execute query
    query_executor(cursor, query, data)
    if cursor.rowcount == 0:
        # If equipment is not in db
        print("\nSorry, the equipment you would like to assign to is not in the database\n")
        return False
    # If equipment is in db
    return True

def verify_username(cursor, username, exp_id):
    """ Verifies that the principle investigator is the correct 
    project lead for the experiment requested"""

    query = ("SELECT ex.* FROM experiment ex\
        INNER JOIN project p ON ex.pro_id = p.pro_id\
        INNER JOIN employee e ON p.proj_leader = e.emp_id\
        WHERE e.emp_id = %s\
            AND ex.exp_id = %s")

    data = (username, exp_id)
    # Execute query
    query_executor(cursor, query, data)
    # If no results are found, print message
    result_set = cursor.fetchall()
    col_names = [i[0] for i in cursor.description]
    print(col_names)
    if result_set:
        # print("\nThank you, you have been verified as the project lead for this experiment\n")
        return True
    else:
        print("\nSorry, you are not the project lead for this experiment\n")
        return False