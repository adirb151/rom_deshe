import sys
import sqlite3
from datetime import datetime, timedelta


# Should be replaced with the real path to db
DB_PATH = r'/home/cluster/orelhaz/bin/rom_deshe/djangonautic/db.sqlite3'


def open_db():
    try:
        sqlite_connection = sqlite3.connect(DB_PATH)
        cursor = sqlite_connection.cursor()
        return sqlite_connection, cursor
    except Exception as e:
        print(e)
        return None, None


def close_db(sqlite_connection, cursor):
    try:
        cursor.close()
        sqlite_connection.close()
        return True
    except Exception as e:
        print(e)
        return False


def add_query(query_target, query_data, cursor, sqlite_connection):
    try:
        if does_exists(query_target):
          print("target already exists!")
          return False
        sqlite_insert_query = """INSERT INTO queries_query
                                          (data, slug, status, name, expiration_date, log, prediction, date, type) 
                                           VALUES 
                                          (?,?,?,?,?,?,?,?,?)"""
        name = query_target
        data = query_data
        slug = name.lower()
        status = 'Running'
        date = datetime.now()
        log = "< " + str(date) + " >: Query added successfully\n"
        prediction = 'TBE'
        expiration_date = date + timedelta(days=3)
        values = (data, slug, status, name, expiration_date, log, prediction, date,"Server")
        cursor.execute(sqlite_insert_query, values)
        sqlite_connection.commit()
        return True
    except Exception as e:
        print(e)
        return False


def update_query(query_target, query_log, cursor, sqlite_connection, failed, done, running):
    try:
        sqlite_log_query = """SELECT log 
                                                  FROM queries_query 
                                                  where name = """ + "'" + query_target + "'"
        cursor.execute(sqlite_log_query)
        curr_log = cursor.fetchone()[0]
        new_log = query_log + '    \n' + curr_log
        sqlite_update_query = """Update queries_query 
                                          set status = ?, log = ? 
                                          where name = ?"""
        status = 'Running'
        if failed:
            status = 'Failed'
        elif done:
            status = 'Success'
        elif running:
            status = 'Running'
        values = (status, new_log, query_target)
        cursor.execute(sqlite_update_query, values)
        sqlite_connection.commit()
        return True
    except Exception as e:
        print(e)
        return False

def process_log(log):
    inf_index = log.find("INFO")
    err_index = log.find("ERROR")
    log = log.strip()
    if inf_index != -1:
        log = log[inf_index:]
    elif err_index != -1:
        log = log[err_index:]
    date_now = str(datetime.now())
    new_log = "< " + date_now + " >: " + log + "\n"
    return new_log
    
def does_exists(target):
    sqlite_connection, cursor = open_db()
    if sqlite_connection is None or cursor is None:
        print("Open db connection failed")
        return False   
    cursor.execute("SELECT name FROM queries_query WHERE name = ?", (target,))
    data=cursor.fetchall()
    if len(data) == 0:
      print("TARGET " + target + " DOES NOT EXISTS")
      return False        
    answer = close_db(sqlite_connection, cursor)
    if not answer:
        print("Close db connection failed")
        return False
    return True
    
def delete_target(target):
    sqlite_connection, cursor = open_db()
    if sqlite_connection is None or cursor is None:
        print("Open db connection failed")
        return False   
    cursor.execute("DELETE FROM queries_query WHERE name = ?", (target,))
    sqlite_connection.commit()      
    answer = close_db(sqlite_connection, cursor)
    if not answer:
        print("Close db connection failed")
        return False
    return True
    
def get_status(target):
    sqlite_connection, cursor = open_db()
    if sqlite_connection is None or cursor is None:
        print("Open db connection failed")
        return False
    cursor.execute("SELECT status FROM queries_query WHERE name = ?", (target,))
    data=cursor.fetchone()
    answer = close_db(sqlite_connection, cursor)
    if not answer:
        print("Close db connection failed")
        return False
    return data[0]

# We run this file with arguments, as follows:
# <case> <target> <data>/<log> DONE/FAILED/RUNNING(optional)
# <case> -  can be ADD or UPDATE - depends if we add a new query or update one
# <target> - target name
# <data>/<log> - data is the query string, log is the log update (depends on the case)
# DONE/FAILED/RUNNING - optional parameters
def main():
    case = sys.argv[1]
    params = sys.argv[2:]
    query_target = params[0]
    sqlite_connection, cursor = open_db()
    if sqlite_connection is None or cursor is None:
        print("Open db connection failed")
        exit(1)
    if case == 'ADD':
        query_data = params[1]
        answer = add_query(query_target, query_data, cursor, sqlite_connection)
        if not answer:
            print("Add query failed")
            exit(1)
    elif case == 'UPDATE':
        query_log = process_log(params[1])
        failed = 'FAILED' in params
        done = 'DONE' in params
        running = 'RUNNING' in params
        prediction = 'TBE'
        answer = update_query(query_target, query_log, cursor, sqlite_connection, failed=failed, done=done, running=running)
        if not answer:
            print("Update query failed")
            exit(1)
    else:
        print("Unknown case - only ADD/UPDATE are allowed")
        exit(1)
    answer = close_db(sqlite_connection, cursor)
    if not answer:
        print("Close db connection failed")
        exit(1)
    print("Changes have been made!")


if __name__ == '__main__':
    main()
