import re
import mysql.connector
import utils
'''
CMPE 138 Team 12 Project: Laboratory

This file contains fucntions that implement all actions that can be carried out by a user in the Lab Associate role. 

'''

'''
    Prints out equipment ordered by monitor
'''
def view_equipment_by_monitor(cursor,user):
    options = """View monitored equipment for:
1. All
2. Others
3. Logged in user
4. Exit
"""
    query = """select emp_lname as 'Last Name', emp_id as 'Employee ID', equ_name as 'Equipment' 
                from (assigned_to JOIN employee as emp on monitor_id = emp_id) 
		                JOIN equipment on assigned_to.equ_id = equipment.equ_id """
    choice = 0
    done = 0
    while(choice!=4 and not done):
        choice = int(input(options))
        if choice == 1:
            query += "order by emp_lname;"
            done = 1
        elif choice == 2:
            emp = str(input("Please enter employee id: "))
            query += "where assigned_to.monitor_id = '" + emp +"';"
            done = 1
        elif choice == 3:
            query += "where assigned_to.monitor_id ='" + user +"';"
            done = 1
        elif choice == 4:
            print("Exiting")
        else:
            print("Please enter a valid option.")

    

    utils.query_executor(cursor,query)
    #num_cols = len(cursor.description)
    #col_names = [i[0] for i in cursor.description]
    #print(col_names)
    json_result, result_set = utils.convert_result_to_json(cursor)
    if len(result_set)==0:
        print("No results found\n")
        return
    else:
        print("Here are all current equipments monitored by lab associate:\n") 
        utils.display_json(json_result)


'''
signup for equipment not currently assigned
'''
def signup_to_monitor(cursor,user):
    #view empty monitored equipment
    print("Here are all current equipments NOT monitored by lab associate:\n")

    #possible to add filter based on experiment
    query = ("""select as_t.equ_id, equ_name
                from assigned_to as as_t join equipment as equ
                    on as_T.equ_id = equ.equ_id
                where monitor_id is null
                order by as_t.equ_id; """)
    utils.query_executor(cursor,query)
    num_cols = len(cursor.description)
    json_result, result_set = utils.convert_result_to_json(cursor)
    for i in result_set:
        print(i)
    #ask user if they want to sign up
    signup = input("\nWould you like to sign up to monitor an equipment?")
    if signup == 'y' or signup == 'Y':
        #ask user for what equipment they want to change
        equ = input("Please enter equipment id:\n")
        if equ in dict(result_set):
            query = """update assigned_to
                    set monitor_id = '%s'
                    where equ_id = '%s'; """ %(user,equ)
            utils.query_executor(cursor,query)
            if cursor.rowcount > 0:
                print("Please check the updated result")
                query = """select as_t.equ_id, equ_name, as_t.monitor_id
                from assigned_to as as_t join equipment as equ
                on as_T.equ_id = equ.equ_id
                where monitor_id = '%s' 
                order by as_t.equ_id; """ %(user)
                utils.query_executor(cursor,query)
                json_result, _ = utils.convert_result_to_json(cursor)
                utils.display_json(json_result)
            else:
                print("Could not update, please try again")
        else:
            print("Equipment id not part of list given, exiting...")

'''
Functionality may need to be removed from lab associate
'''
def signup_to_maintain(cursor):
    pass
    
def view_current_allocation(cursor,user):
    
    options = """View current equipment monitor for:
1. All
2. Specific Equipment
3. Logged in user
4. Exit
"""
    query = """select equ_name as 'Equipment', exp_sdate as 'Start Date',emp_lname as 'Last Name' 
                from (assigned_to JOIN employee as emp on monitor_id = emp_id) 
		        JOIN equipment on assigned_to.equ_id = equipment.equ_id"""
    choice = 0
    done = 0
    while(choice!=4 and not done):
        choice = int(input(options))
        if choice == 1:
            query += """ where exp_edate is null
            order by equ_name;"""
            done = 1
        elif choice == 2:
            equ = str(input("Please enter equipment id: "))
            query += " where exp_edate is null and assigned_to.equ_id = '" + equ +"';"
            done = 1
        elif choice == 3:
            query += " where exp_edate is null and assigned_to.monitor_id ='" + user +"';"
            done = 1
        elif choice == 4:
            print("Exiting")
        else:
            print("Please enter a valid option.")

    utils.query_executor(cursor,query)
    #num_cols = len(cursor.description)
    #col_names = [i[0] for i in cursor.description]
    #print(col_names)
    json_result, result_set = utils.convert_result_to_json(cursor)
    if len(result_set)==0:
        print("No results found\n")
        return
    else:
        print("Here are current allocated equipment:\n")  
        utils.display_json(json_result)

    
def getSdateEdate():
    sdate = input("Start Date('YYYY-MM-DD'):")
    edate = input("End Date('YYYY-MM-DD'):")
    return sdate,edate


def view_past_allocation(cursor,user):
    query = ("""select equ_name as 'Equipment', exp_sdate as 'Start Date',exp_edate as 'End Date',emp_lname as 'Last Name' 
                from (assigned_to JOIN employee as emp on monitor_id = emp_id) 
		        JOIN equipment on assigned_to.equ_id = equipment.equ_id\n""")

    options = """Filter past equipment allocation by: 
1. Start Date
2. End Date
3. Equipment ID
4. None
5. Exit
"""
    choice = 0
    done = 0
    sdate = ''
    edate = ''
    while(choice !=5 and not done):
        choice = int(input(options))
        if choice == 1:
            sdate,edate = getSdateEdate()
            query += """where  exp_sdate >='%s'and  exp_sdate <= '%s' and exp_edate is not null
                order by equ_name;""" %(edate,sdate)
            done = 1
        elif choice == 2:
            sdate,edate = getSdateEdate()
            query += """where exp_edate >='%s' and exp_edate <= '%s' and exp_edate is not null
                order by equ_name;""" %(edate,sdate)
            done = 1
        elif choice == 3:
            equ_id = input("Equipment ID: ")
            query += """where equipment.equ_id='%s' 
                order by equ_name"""%(equ_id)
            done = 1
        elif choice == 4:
            query += """where exp_edate is not null
                order by equ_name;"""
            done = 1
        elif choice == 5:
            print("Exiting")
        else:
            print("Please enter a valid option.")
    
    utils.query_executor(cursor,query)
    #num_cols = len(cursor.description)
    #col_names = [i[0] for i in cursor.description]
    #print(col_names)
    json_result, result_set = utils.convert_result_to_json(cursor)
    if len(result_set)==0:
        print("No results found\n")
        return
    else:
        print("Here are past allocated equipment:\n")  
        utils.display_json(json_result)



def la_handler(cursor,user):
    
    options_array = [   ("View Equipment By Monitor",view_equipment_by_monitor,),
                    ("Equipment Monitor Signup",signup_to_monitor), 
                    ("View Current Equipment Monitor",view_current_allocation), 
                    ("View Past Equipment Monitor",view_past_allocation),
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
