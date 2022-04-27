# SJSU CMPE 138 Fall 2021 TEAM12
'''
CMPE 138 Team 12 Project: Laboratory
This file contains fucntions that implements all actions that can be carried out by a user in the Research Scientist role.
'''
import utils
options_string = """Please select the following options by entering the number for the action to continue:
1.  Signup for Experiment
2.  Signup for Trial
3.  Signup for Publication
4.  View current Project Status
5.  View trial Participants
6.  Delete Trial Participant
7.  Exit """

exit_string = """ You have chosen to exit. Please relaunch the app to continue"""


def rs_handler(cursor,username):
    choice = 0

    while (choice != 7):
        choice = int(input(options_string))

        if choice == 1:
            signup_experiment(cursor, username)

        elif choice == 2:
            signup_trial(cursor, username)

        elif choice == 3:
            signup_publication(cursor,username)

        elif choice == 4:
            view_current_status_project(cursor,username)

        elif choice == 5:
            view_trial_participant(cursor,username)

        elif choice == 6:
            delete_trial_participant(cursor,username)

        elif choice == 7:
            print(exit_string)
            break    

        else:
            print("Please enter a valid option.")


def signup_experiment(cursor, username):
    print("Here are all available ongoing experiments:\n")

    query = ("""select exp_id as 'ID', exp_name as 'Experiment' 
                from experiment
                where trial_flag = 0 and (exp_status = 'ongoing' or exp_status = 'planned')
                order by exp_id; """)
    utils.query_executor(cursor,query)
    json_result, result_set = utils.convert_result_to_json(cursor)
    if len(result_set) < 1:
        print("No available experiment right now.")
        return
    utils.display_json(json_result)
    #ask user if they want to sign up
    signup = input("\nWould you like to sign up to an experiment?")
    if signup == 'y' or signup == 'Y':
        #ask user for what experiment they want to sign up for
        exp = input("Please enter experiment id:\n")
        if exp in dict(result_set):
            #check if they already signed up for that experiment
            checkquery = "select exp_id from conducts_experiments where emp_id='%s' and exp_id='%s'; "%(username,exp)
            utils.query_executor(cursor,checkquery)
            json_result_check, result_set_check = utils.convert_result_to_json(cursor)
            if username in result_set_check:
                print("Already signed up for this experiment")
                return
            query = """insert conducts_experiments values 
                    ('%s','%s'); """ %(username,exp)
            utils.query_executor(cursor,query)
            #check and display if changes were made
            if cursor.rowcount > 0:
                print("Please check your current experiments")
                query = """select E.exp_name as 'Signed up Experiment' 
                from conducts_experiments as CE JOIN experiment as E 
                on CE.exp_id = E.exp_id 
                where CE.emp_id = '%s' 
                order by E.exp_name; """ %(username)
                utils.query_executor(cursor,query)
                json_result, _ = utils.convert_result_to_json(cursor)
                utils.display_json(json_result)
            else:
                print("Could not update, please try again")
        else:
            print("Experiment id not part of list given, exiting...")


def signup_trial(cursor, username):
    print("Here are all available ongoing trials:\n")

    query = ("""select exp_id as 'ID', exp_name as 'Experiment' 
                from experiment
                where trial_flag = 1 and (exp_status = 'ongoing' or exp_status = 'planned')
                order by exp_id; """)
    utils.query_executor(cursor,query)
    json_result, result_set = utils.convert_result_to_json(cursor)
    if len(result_set) < 1:
        print("No available trial right now.")
        return
    utils.display_json(json_result)
    #ask user if they want to sign up
    signup = input("\nWould you like to sign up to an trial?")
    if signup == 'y' or signup == 'Y':
        #ask user for what experiment they want to sign up for
        exp = input("Please enter trial id:\n")
        if exp in dict(result_set):
            #check if they already signed up for that experiment
            checkquery = "select exp_id from conducts_trials where emp_id='%s' and exp_id='%s'; "%(username,exp)
            utils.query_executor(cursor,checkquery)
            json_result_check, result_set_check = utils.convert_result_to_json(cursor)
            if username in result_set_check:
                print("Already signed up for this experiment")
                return
            query = """insert conducts_trials values 
                    ('%s','%s'); """ %(username,exp)
            utils.query_executor(cursor,query)
            #check and display if changes were made
            if cursor.rowcount > 0:
                print("Please check your current trials")
                query = """select E.exp_name as 'Signed up trial' 
                from conducts_trials as CT JOIN experiment as E 
                on CT.exp_id = E.exp_id 
                where CT.emp_id = '%s' 
                order by E.exp_name; """ %(username)
                utils.query_executor(cursor,query)
                json_result, _ = utils.convert_result_to_json(cursor)
                utils.display_json(json_result)
            else:
                print("Could not update, please try again")
        else:
            print("Trial id not part of list given, exiting...")

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


def view_current_status_project(cursor, username):
    print("Please Select an option")
    options = """View current project for
1. ALL info related to Project
2. Experiment related to Project
3. Trial related to Project
4. Publication related to Project
5. Cancel\n"""
    choice = ""
    while choice != "6":
        choice = str(input(options))
        if choice == '1':
            # Display all projects
            query = ("SELECT * FROM Project")
            utils.query_executor(cursor, query)
            json, result_set = utils.convert_result_to_json(cursor)
            utils.display_json(json)
            # User selects a project id
            id = str(input("Please enter Project ID: "))
            query = ("SELECT e.*, p.*\
                FROM experiment as e join project as p on e.pro_id = p.pro_id\
                        WHERE p.pro_id = %s")
            data = (id,)
            utils.query_executor(cursor, query, data)
            json, result_set = utils.convert_result_to_json(cursor)
            if len(result_set)==0:
                print("No results found\n")
                return
            utils.display_json(json)
        elif choice == '2':
            # Display all projects
            query = ("SELECT * FROM Project")
            utils.query_executor(cursor, query)
            json, result_set = utils.convert_result_to_json(cursor)
            utils.display_json(json)
            id = str(input("Please enter Project ID: "))
            query = ("SELECT e.*\
                FROM experiment e INNER JOIN Project p ON e.pro_id = p.pro_id\
                        WHERE p.pro_id = %s")
            data = (id,)
            utils.query_executor(cursor, query, data)
            json, result_set = utils.convert_result_to_json(cursor)
            if len(result_set)==0:
                print("No results found\n")
                return
            utils.display_json(json)
        elif choice == '3':
            # Display all projects
            query = ("SELECT * FROM Project")
            utils.query_executor(cursor, query)
            json, result_set = utils.convert_result_to_json(cursor)
            utils.display_json(json)
            # Enter project id
            id = str(input("Please enter Project ID: "))
            query = ("SELECT t.*\
                FROM trial t INNER JOIN experiment e ON t.exp_id = e.exp_id\
                    INNER JOIN project p ON e.pro_id = p.pro_id\
                        WHERE p.pro_id = %s")
            data = (id,)
            utils.query_executor(cursor, query, data)
            json, result_set = utils.convert_result_to_json(cursor)
            if len(result_set)==0:
                print("No results found\n")
                return
            utils.display_json(json)
            
        elif choice == '4':
            # Display all projects
            query = ("SELECT * FROM Project")
            utils.query_executor(cursor, query)
            json, result_set = utils.convert_result_to_json(cursor)
            utils.display_json(json)
            # Enter project id
            # Publication information
            id = str(input("Please enter Project ID: "))
            query = ("SELECT pb.*\
                    FROM publication pb INNER JOIN project p ON p.pro_id = pb.pro_id\
                            WHERE p.pro_id = %s")
            data = (id,)
            utils.query_executor(cursor, query, data)
            json, result_set = utils.convert_result_to_json(cursor)
            if len(result_set)==0:
                print("No results found\n")
                return
            utils.display_json(json)
            
        elif choice == '5':
            print("Exiting")
            return
        else:
            print("Please enter a valid option.")
            break


def view_trial_participant(cursor,username):
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
