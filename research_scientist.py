'''
CMPE 138 Team 12 Project: Laboratory

This file contains fucntions that implements all actions that can be carried out by a user in the Research Scientist role.

'''
import utils
options_string = """Please select the following options by entering the number for the action to continue:
1.  Signup for Experiment
2.  Signup for Trial
3.  Signup for Publication
4.  View current status for Experiment, Trial, and Publication
5.  View current Project
6.  View trial Participants
7.  Delete Trial Participant
8.  Exit """

exit_string = """ You have chosen to exit. Please relaunch the app to continue"""


def rs_handler(cursor,username):
    choice = 0

    while (choice != 7):
        choice = int(input(options_string))

        if choice == 1:
            signup_experiment(cursor)

        elif choice == 2:
            signup_trial(cursor)

        elif choice == 3:
            signup_publication(cursor,username)

        elif choice == 4:
            #view_current_status(type_to_view, params)
            pass
        elif choice == 5:
            view_current_status_project(cursor)

        elif choice == 6:
            view_trial_participants(cursor,username)

        elif choice == 7:
            delete_trial_participant(cursor,username)

        elif choice == 8:
            print(exit_string)
            break    

        else:
            print("Please enter a valid option.")


def signup_experiment(cursor):
    id = str(input("Please enter your Employee ID: "))
    cursor.execute ("SELECT emp_id FROM Employee where emp_id=%s", (id,))
    result_set = cursor.fetchall()
    name = str(input("Please enter the experiment that you would like to work out: "))
    if result_set:
        print ("Your Employee ID is " + result_set + "and your experiment is " + name)
        print ("Your information will be reviewed by one of our Principle Investigator")




def signup_trial(cursor):
    pass

def signup_publication(cursor,username):
    _input1 = str(input("\nPlease enter publication id : "))
    query1="SELECT emp_id,pub_id From  drafts where emp_id='%s' AND pub_id='%s'" %(username,_input1)
    if not utils.query_executor(cursor, query1):
        return
    json_result, result_set = utils.convert_result_to_json(cursor)
    if(result_set==''):
        print("you are already in publication")
    else:
        query="SELECT pub_id FROM publication where pub_id='%s'" %(_input1)
        if not utils.query_executor(cursor, query):
            return
        json_result1, result_set1 = utils.convert_result_to_json(cursor)
        if(_input1==result_set1[0][0]):
            query="INSERT INTO drafts (emp_id,pub_id) VALUES ('%s', '%s')" %(username,_input1)
            if not utils.query_executor(cursor, query):
                return
            print('your signed up for publication')
        else:
            print("there is something wrong with publication id")

def view_current_status(type_to_view, params):
    pass

# Same function implements for experiment, publication and trial

def view_current_status_project(cursor):
    query = 'SELECT pro_id, pro_name, status, security_level, pro_sdate, pro_edate, pro_cost, PI FROM project '
    cursor.execute(query)
    result_set = cursor.fetchall()
    print("These are the information of the project :")
    if cursor.rowcount > 0:
        for i in result_set:
            print(i)
        else:
            print("Sorry, your query has no matching results")


def view_trial_participants(cursor,username):
    _input1 = str(input("\nPlease enter experiment id : "))
    query1="SELECT conducts_trials.emp_id,exp_id FROM laboratory.conducts_trials INNER JOIN laboratory.works_on ON works_on.emp_id=conducts_trials.emp_id having emp_id='%s' AND exp_id='%s'" %(username,_input1)
    if not utils.query_executor(cursor, query1):
        return
    json_result, result_set = utils.convert_result_to_json(cursor)
    if(_input1!=''):
        query="SELECT ts_fname,ts_lname,test_subject.ts_id FROM test_subject inner join participates on test_subject.ts_id=participates.ts_id WHERE participates.exp_id='%s'" %(_input1)
    
        if not utils.query_executor(cursor, query):
            return
        json_result1, _= utils.convert_result_to_json(cursor)
    #    result_set = cursor.fetchall()
        print("\nFollowing are the results of your search query:\n")
        if cursor.rowcount > 0:
            utils.display_json(json_result1)
        else:
            print("Sorry, your query has no matching results in the database.")
    else:
        print("your experiment id is invalid")



def delete_trial_participant(cursor,username):
    _input1 = str(input("\nPlease enter experiment id : "))
    query1="SELECT conducts_trials.emp_id,exp_id FROM laboratory.conducts_trials INNER JOIN laboratory.works_on ON works_on.emp_id=conducts_trials.emp_id having emp_id='%s' AND exp_id='%s'" %(username,_input1)
    if not utils.query_executor(cursor, query1):
        return
    json_result, result_set1 = utils.convert_result_to_json(cursor)
    if(_input1!=''):
        _input = str(input("\nPlease enter the test id that you want to delete: "))
        query2=" SELECT ts_id from test_subject WHERE ts_id='%s'" %(_input)
        if not utils.query_executor(cursor, query2):
            return
        json_result2, result_set2 = utils.convert_result_to_json(cursor)
        if(_input==result_set2[0][0]):
            query = "DELETE FROM participates WHERE ts_id= '%s' AND exp_id='%s'" %(_input,_input1)
            if not utils.query_executor(cursor, query):
                return
        else:
            print("you put wrong test id")
    else:
        print("you put wrong experiment id")
