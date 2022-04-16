'''
CMPE 138 Team 12 Project: Laboratory
This file contains fucntions that implement all actions that can be carried out by a user in the Test Subject role. 
'''
import utils
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
    
    # make sure be default the test subject can only search for trials that are NOT done,
    # and trials for which they are withing the age range and match the gender requirements. 
    # i.e test subejcts should only be able to look at trials they are eligible for.
    
    print("Here are the columns of the table you have chosen to query:\n")
    
    query = ("SELECT * FROM trial")
    cursor.execute(query)
    num_cols = len(cursor.description)
    col_names = [i[0] for i in cursor.description]
    
    print(col_names)
    
    field_name = str(input("\nPlease enter the field by which you would like to search: "))
    
    if field_name not in col_names:
        print("Incorrect field name. Please choose again.")
        return
        
    field_filter = str(input("Please enter the value of the field to filter by: "))
    
    query = 'SELECT * FROM trial WHERE {} = %s'.format(field_name)
    cursor.execute(query, (field_filter,))
    result_set = cursor.fetchall()
    
    print("\nFollowing are the results of your search query:\n")
    if cursor.rowcount > 0:
        for i in result_set:
            print(i)
    else:
        print("Sorry, your query has no matching results in the database.")
    
        
    
def participate_in_trial(cursor,username):
    _input1 = str(input("\nPlease enter experiment id : "))
    query1="SELECT exp_id FROM trial WHERE exp_id='%s'" %(_input1)
    if not utils.query_executor(cursor, query1):
        return
    json_result1, result_set1 = utils.convert_result_to_json(cursor)  
    query2="SELECT ts_id FROM test_subject WHERE ts_id='%s'" %(username)
    if not utils.query_executor(cursor, query2):
        return
    json_result2, result_set2 = utils.convert_result_to_json(cursor)  
    if(_input1==result_set1[0][0] and username==result_set2[0][0]):
        query3="INSERT INTO participates (exp_id,ts_id) VALUES ('%s', '%s')" %(_input1,username)
        if not utils.query_executor(cursor, query3):
            return
        print("You have been added to your desired trial")
    else:
        print("your test id or your experiment id is wrong")
    
    
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
        print('you are no longer in this trial')
    else:
        print("you entered wrong test_id")



