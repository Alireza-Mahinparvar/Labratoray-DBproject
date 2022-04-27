# SJSU CMPE 138 Fall 2021 TEAM12
'''
CMPE 138 Team 12 Project: Laboratory
This file contains fucntions that implement all actions that can be carried out by a user in the Test Subject role. 
'''
import utils
import datetime
from dateutil.relativedelta import relativedelta
options_string = """Please select from the following actions allowed for your role by entering the number for the action:
1. Search trials
2. Participate in a trial
3. Withdraw from a trial
4. Exit\n"""

exit_string = """You have chosen to EXIT so the databse application will close now. Please relaunch the app if you want to continue."""

def ts_handler(cursor, username):
    
    choice = 0
    
    while (choice != 4):
        choice = int(input(options_string))
        
        if choice == 1:
            search_trial(cursor, username)
        
        elif choice == 2:
            participate_in_trial(cursor, username)
            
        elif choice == 3:
            withdraw_from_trial(cursor, username)
        
        elif choice == 4:
            print(exit_string)
            break
            
        else:
            print("Please enter a valid number.")
            
        
def search_trial(cursor, username):
    
    criteria = input("Please provide the criteria you would like to search trials by: ")
    query1 = "SELECT ts_dob FROM test_subject WHERE ts_id=%s"
    
    if not utils.query_executor(cursor, query1, (username,)):
        return
      
    age = 0
    result = cursor.fetchone()
    if cursor.rowcount > 0:
        dob = result[0]
        time_delta = relativedelta(datetime.date.today(), dob)
        age = int(time_delta.years)
    else:
        return
        
    query2 = "SELECT * FROM trial WHERE criteria LIKE %s AND agerange_start < %s AND agerange_end > %s"
    criteria_new = "%" + criteria + "%"
    if not utils.query_executor(cursor, query2, (criteria_new, age, age)):
        return
    
    print("\nFollowing are the trials you are eligible for: \n")
    json_result, result_set = utils.convert_result_to_json(cursor)
    if len(result_set) < 1:
        print("There are no trials you are eligible for.")
        return
        
    utils.display_json(json_result)
    
    
def participate_in_trial(cursor,username):
    _input1 = str(input("\nPlease enter id of trial you would like to sign up for: "))
    
    query1="SELECT num_allowed_participants FROM trial WHERE exp_id='%s'" %(_input1)
    if not utils.query_executor(cursor, query1):
        return
        
    result = cursor.fetchone()
    num_allowed_participants = 0
    if cursor.rowcount > 0:
        num_allowed_participants = result[0]
    else:
        return
        
    query2="SELECT COUNT(*) FROM participates WHERE exp_id='%s'" %(_input1)
    if not utils.query_executor(cursor, query2):
        return
      
    num_participants = 0
    result = cursor.fetchone()
    if cursor.rowcount > 0:
        num_participants = result[0]
    else:
        return
        
    if num_participants >= num_allowed_participants:
        print("Sorry, the trial you selected is already full and thus you cannot participate in it.")
        return
    else:
        check_query = "SELECT * FROM participates WHERE ts_id = %s AND exp_id = %s"
        if not utils.query_executor(cursor, check_query, (username, _input1)):
            return
        result = cursor.fetchone()
        if cursor.rowcount > 0:
            print("You have already signed up for this trial.\n")
            return
        query3="INSERT INTO participates (exp_id,ts_id) VALUES ('%s', '%s')" %(_input1,username)
        if not utils.query_executor(cursor, query3):
            return
        print("You have been added to your desired trial!\n")
        verification_query = "SELECT * FROM participates WHERE ts_id=%s AND exp_id=%s"
        if not utils.query_executor(cursor, verification_query, (username, _input1)):
            return
        json_result, result_set = utils.convert_result_to_json(cursor)
        utils.display_json(json_result)
        
        
    
def withdraw_from_trial(cursor,username):
    _input1 = str(input("\nPlease enter experiment id : "))
    query1="SELECT exp_id,ts_id FROM participates WHERE exp_id='%s' AND ts_id='%s'" %(_input1,username)
    if not utils.query_executor(cursor, query1):
        return
    json_result, result_set1 = utils.convert_result_to_json(cursor)  
    if(_input1==str(result_set1[0][0])):
        query="DELETE FROM participates WHERE ts_id= '%s' AND exp_id='%s'" %(username,_input1)
        if not utils.query_executor(cursor, query):
            return
        print('You are no longer in this trial. \n')
    else:
        print("You entered wrong test_id. \n")