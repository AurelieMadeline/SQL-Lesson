import sqlite3

DB = None
CONN = None

def get_student_by_github(github):
    # Assign the variable query to the DB query we want to run
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""  #no need for ; here.  The '?' is a placeholder and is used much like the %.
    
    # Executing the query above:
    DB.execute(query, (github,))    # this is where we give the '?' some variable.  It has to be given as a tuple, even though only one 'github' is needed.
    
    #fetch row from the table 'DB' one at a time until it finds the github name
    row = DB.fetchone() # row is returned as a tuple (a, b)
    print """\
Student: %s %s
Github account: %s"""%(row[0], row[1], row[2])

def get_project_by_title(title):
    query = """SELECT title, description, max_grade FROM Projects WHERE title = ?"""
    DB.execute(query, (title,))
    row = DB.fetchone()
    print """\
Title:  %s
Description:  %s
Max Grade:  %s """ % (row[0], row[1], row[2])

def make_new_student(first_name, last_name, github):
    query = """INSERT into Students values (?, ?, ?)"""  #The Students table has 3 columns, so when we insert information, we want to give info for each column
    DB.execute (query, (first_name, last_name, github))
    CONN.commit()   # b/c this is a brand new entry into the DB, we have to commit it
    print "Successfully added student: %s %s" % (first_name, last_name)

def make_new_project(title, description, max_grade):
    query = """INSERT into Projects (title, description, max_grade) values (?, ?, ?)"""
    DB.execute (query, (title, description, max_grade))
    CONN.commit()
    print "Successfully added a project: %s - %s; max grade %d" % (title, description, int(max_grade))

def get_grade_by_project_and_name (last_name, project_title):
    query = """SELECT Students.last_name, Projects.project_title, Projects.grade FROM Students JOIN Projects ON (Students.github = Grades.student_github) WHERE last_name=? AND project_title=?"""
    DB.execute (query,(last_name, project_title))
    row = DB.fechone()
    print "%s received a %s on %s" % (row[0], row[2], row[1])

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()

def main():     # This is the first function run by the program, calling other functions above
    connect_to_db()
    command = None
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split(",")
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            get_student_by_github(*args) 
        elif command == "new_student":
            make_new_student(*args)
        elif command == "project":
            get_project_by_title(*args)
        elif command == "new_project":
            make_new_project(*args)
        elif command == "project_grade":
            get_grade_by_project_and_name(*args)

    CONN.close() # closing connection to our database

if __name__ == "__main__":
    main()
