'''
CMPE 138 Team 12 Project: Laboratory
This file contains fucntions faciliate input + output parsing and formatting as well as password handling.
'''


import logging
import mysql.connector
import json
from rich.console import Console
from rich import print_json
from rich.table import Table

console = Console()

def query_executor(cursor, query, values=None):

    try:
        if values is not None:
            cursor.execute(query, values)
        else:
            cursor.execute(query)
        transaction = cursor.statement
        rows_affected = "{} row(s) affected".format(cursor.rowcount)
        logging.info("\n" + transaction + "\n" + rows_affected)
    except mysql.connector.Error as err:
        print("Something went wrong for the query you requested: {}".format(err))
        logging.debug("Something went wrong for the query you requested: {}".format(err))
        logging.debug(query)
        return False

    return True


def convert_result_to_json(cursor):
    rows_affected = cursor.rowcount
    if rows_affected < 1:
        return json.dumps(list(dict()), default=str), list(tuple())
    col_names = [i[0] for i in cursor.description]
    result_set = cursor.fetchall()
    jsonDB = []
    jsonDBList = []
    for result in result_set:
        jsonDB.append(dict(zip(col_names, result)))
        jsonDBList.append(result)
    return json.dumps(jsonDB, default=str), result_set


def display_json(jsonDB):
    # For backup
    # console.print_json(jsonDB)

    d = json.loads(jsonDB)
    if len(d) < 1:
        return
    table = Table(show_header=True)

    for key in d[0]:
        table.add_column(str(key), no_wrap=True)

    for ele in d:
        templist = list(ele.values())
        newstrlits = []
        for val in templist:
            newstrlits.append(str(val))
        table.add_row(*newstrlits)

    console.print(table)

def getChoice(options_string):
    return int(input(options_string) or 0)
