Student Database: Comp3005 Q3 P1
A command-line Python application that connects to a PostgreSQL database and performs Create, Read, Update and Delete (CRUD) operations on a students table

Demo Link: https://www.youtube.com/watch?v=XSTqCTGF994

Repository Structure

├── README.md          This file \
├── app.py             The application \
└── database/ \
   &emsp; └── setup.sql      Creates the students table and inserts the initial data\

Database Schema

Table students:

Column	     &emsp;&emsp; &emsp;&emsp;      Type and constraints \
student_id	   &emsp; &emsp; &emsp;   SERIAL, PRIMARY KEY (auto-increment)\
first_name	    &emsp;&emsp; &emsp;   TEXT, NOT NULL \
last_name	   &emsp;  &emsp;  &emsp; TEXT, NOT NULL \
email	       &emsp;  &emsp;&emsp;   TEXT, NOT NULL, UNIQUE \
enrollment_date	 &emsp;   DATE \

Initial data 

first_name	last_name	email	                enrollment_date
John	    Doe	        john.doe@example.com	2023-09-01
Jane	    Smith	    jane.smith@example.com	2023-09-01
Jim	        Beam	    jim.beam@example.com	2023-09-02

Setup
1. Create the database and table

-> Create a database named school, then run database/setup.sql against it.

-> Using pgAdmin:

a. Right-click Databases, choose Create, then Database, name it school and save.
b. Select school, open Tools, then Query Tool.
c. Paste the contents of database/setup.sql and run it (F5).

Optional: Check the result with SELECT * FROM students;

2. Install Python Driver

- This allows Python to communicate with the databse server

"python3 -m pip install psycopg2-binary"

3. Check connection settings

The connection settings are in DB_CONFIG listed on line 15 of app.py.
Ensure they match your devices.

OR

Connect to server thorugh an SSH tunnel

"ssh -N -L 5433:localhost:5432 <username>@<server-ip>"

-> This is what I did, so the port 5432 does not need to be changed in the code.

4. Run application: "python3 app.py"
