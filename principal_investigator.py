'''
CMPE 138 Team 12 Project: Laboratory

This file contains fucntions that implement all actions that can be carried out by a user in the Principal Investigator role. 

'''

import utils
def pi_handler():
    pass
    
def create_project():
    pass
    
    
def create_experiment():
    pass
    
    
def create_trial():
    pass 
    
    
def create_publication():
    pass
    
    
def assign_rs_to_proj():
    pass
    
    
def update_project():
    pass
    
    
def update_experiment():
    pass
    
    
def update_trial():
    pass
    

def update_publication():
    pass
    
def approve_publication(cursor,username):
    _input1 = str(input("\nPlease enter publication id : "))
    _input2 = str(input("\nPlease enter publication approval date : "))
    query1="UPDATE publication SET approved_by = '%s',approved_date='%s',date_published='%s' WHERE pub_id='%s'" %(username,_input2,_input2,_input1)
    if not utils.query_executor(cursor, query1):
        return
    
def approve_trial(cursor,username):
    approve_experiment()

def approve_experiment():
    pass
    
    
def view_table():
    # this will implement all three depending on input
    pass

def view_work_allocation_for_rs():
    pass
    
    
def view_equipment_allocation():
    pass
    
def assign_equipment():
    pass
    
def update_equipment_assignment():
    pass
    
    
    
    
    
