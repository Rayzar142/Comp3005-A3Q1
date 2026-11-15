"""
Student database app: connects to a PostgreSQL database and performs CRUD
operations on the students table.
"""

import os
import getpass
# Database driver, let's ypthon talk to Postgre
import psycopg2
# Catches error names
from psycopg2 import errors

# Connection settings. Host/port point at the SSH tunnel on this machine.
# This code connects the laptop to the PostgreSQL server.
DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "port": int(os.environ.get("DB_PORT", 5433)),
    "dbname": os.environ.get("DB_NAME", "school"),
    "user": os.environ.get("DB_USER", "postgres"),
}

# password delcared 
password = None


def get_connection():
    """
    Open and return a new connection to the database.

    The password is requested once and remembered for this run
    """
    # global variable
    global password

    if password is None:
        password = getpass.getpass("Database password: ")
    return psycopg2.connect(password=password, **DB_CONFIG)


def getAllStudents():
    """
    Retrieve every record from the students table and print it as a table.
    """
    # Safety check, For 'finally' at the end of the function to check if a connection was opened.
    conn = None
    try:
        # Try to open a connection to the db server
        conn = get_connection()

        # 'with' closes the cursor automatically when the block ends
        # cursor acts as a an object that sends and receives queries 
        with conn.cursor() as cur:
            # cur.execute is what sends the query to the database, the results are inside cur
            cur.execute(
                "SELECT student_id, first_name, last_name, email, enrollment_date "
                "FROM students ORDER BY student_id;"
            )
            # Returns the rows as tuples
            rows = cur.fetchall() 

        # Prints the output to look nice
        print(f"{'ID':<4} {'First':<12} {'Last':<12} {'Email':<28} {'Enrolled'}")
        print("-" * 70)
        for student_id, first, last, email, enrolled in rows:
            print(f"{student_id:<4} {first:<12} {last:<12} {email:<28} {enrolled or ''}")
        # print(f"({len(rows)} students)") - Debugging
        return rows
    
    except psycopg2.Error as e:
        # Prints the error type
        print(f"Database error in getAllStudents: {e}")

    finally:
        # Closes any connection that was opened.
        if conn is not None:
            conn.close()


def addStudent(first_name, last_name, email, enrollment_date):
    """
    Insert a new student record into the students table.

    student_id is not supplied: the SERIAL column generates it automatically.
    enrollment_date should be a string in YYYY-MM-DD format.
    """
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            # %s placeholders keep the values separate from the SQL text, and also stops SQL injection
            cur.execute(
                "INSERT INTO students (first_name, last_name, email, enrollment_date) "
                "VALUES (%s, %s, %s, %s);",
                (first_name, last_name, email, enrollment_date),
            )

        #commits the new info to the database
        conn.commit()  

        # Print added student
        print(f"Added student: {first_name} {last_name} ({email}), enrolled {enrollment_date}")

    except errors.UniqueViolation:
        # Since we treat email as a unique element, catch if there are duplicates. (rollback() 'undoes' the action)
        conn.rollback()
        print(f"Error: a student with the email '{email}' already exists.")

    except psycopg2.Error as e:
        # Any errors that are not due to unique error are undone
        if conn is not None:
            conn.rollback()  
        print(f"Database error in addStudent: {e}")

    finally:
        if conn is not None:
            conn.close()

def updateStudentEmail(student_id, new_email):
    """
    Update the email address of the student with the given student_id.
    """
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute(
                # Where specifies student
                "UPDATE students SET email = %s WHERE student_id = %s;",
                (new_email, student_id),
            )

            '''rowcount = how many rows the UPDATE changed. If none were changed that means the student 
            associated with the id didnt exist '''

            if cur.rowcount == 0:
                print(f"No student found with ID {student_id}.")
                conn.rollback()
                return
            
        conn.commit() 
        print(f"Updated student {student_id}: new email is {new_email}")

    except errors.UniqueViolation:
        # Unique Error
        conn.rollback()
        print(f"Error: the email '{new_email}' is already used by another student.")

    except psycopg2.Error as e:
        if conn is not None:
            conn.rollback()
        print(f"Database error in updateStudentEmail: {e}")

    finally:
        if conn is not None:
            conn.close()

def deleteStudent(student_id):
    """
    Delete the student record with the given student_id.
    """
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM students WHERE student_id = %s;",
                # comma makes it a one item tuple, without it there are a lot of errors
                (student_id,), 
            )

            # Feedback to see if anything was changed
            if cur.rowcount == 0:
                print(f"No student found with ID {student_id}.")
                conn.rollback()
                return

        # success
        conn.commit() 
        print(f"Deleted student with ID {student_id}.")

    except psycopg2.Error as e:
        if conn is not None:
            conn.rollback()
        print(f"Database error in deleteStudent: {e}")

    finally:
        if conn is not None:
            conn.close()

def main():
    """
    Text menu for ease of use
    """
    while True:
        print("\n=== Student Database ===")
        print("1. Show all students")
        print("2. Add a student")
        print("3. Update a student's email")
        print("4. Delete a student")
        print("5. Quit")
        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            getAllStudents()

        elif choice == "2":
            first = input("First name: ").strip()
            last = input("Last name: ").strip()
            email = input("Email: ").strip()
            date = input("Enrollment date (YYYY-MM-DD): ").strip()

            if not first or not last or not email or not date:
                print("All fields are required.")
            else:
                addStudent(first, last, email, date)

        elif choice == "3":
            try:
                student_id = int(input("Student ID: "))
            except ValueError:
                print("Student ID must be a whole number.")
                # Go back to menu
                continue  

            new_email = input("New email: ").strip()
            if not new_email:
                print("Email cannot be empty.")
            else:
                updateStudentEmail(student_id, new_email)

        elif choice == "4":
            try:
                student_id = int(input("Student ID: "))

            except ValueError:
                print("Student ID must be a whole number.")
                continue
            deleteStudent(student_id)

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid choice, please enter a number from 1 to 5.")

if __name__ == "__main__":
    main();
