## Lidsyda NOuanphachan
## Class CNE340 Winter 2025

import mysql.connector
import time
import json
import requests
from datetime import date
import html2text


# Connect to database
# You may need to edit the connect function based on your local settings.#I made a password for my database because it is important to do so. Also make sure MySQL server is running or it will not connect
def connect_to_sql():
    conn = mysql.connector.connect(user='root', password='',
                                   host='127.0.0.1', database='cne340')
    return conn


# Create the table structure
def create_tables(cursor):
    # Creates table
    # Must set Title to CHARSET utf8 unicode Source: http://mysql.rjweb.org/doc.php/charcoll.
    # Python is in latin-1 and error (Incorrect string value: '\xE2\x80\xAFAbi...') will occur if Description is not in unicode format due to the json data
    cursor.execute("""CREATE TABLE IF NOT EXISTS jobs (id INT PRIMARY KEY AUTO_INCREMENT,Job_id VARCHAR(50) NOT NULL,company VARCHAR(300),Created_at DATE,url VARCHAR(2000),Title TEXT,Description TEXT,
    UNIQUE (Job_id)""");

# Query the database.
# You should not need to edit anything in this function
def query_sql(cursor, query):
    cursor.execute(query)
    return cursor


# Add a new job
def add_new_job(cursor, job_details):
    """Insert a new job into the jobs table."""
    # extract all required columns
    cursor.execute("INSERT INTO jobs(job_title, description) VALUES(%s, %s)",job_details)

# Check if new job
def check_if_job_exists(cursor, jobdetails):
    job_id = jobdetails['id']
    query = f"SELECT * FROM jobs WHERE Job_id = '{job_id}'"
    cursor.execute(query)
    return cursor.fetchall()

# Deletes job
def delete_job(cursor, jobdetails):
    job_id = jobdetails['id']
    query = f"DELETE FROM jobs WHERE Job_id = '{job_id}'"
    cursor.execute(query)
    cursor.connection.commit()
    print(f"Job with ID {job_id} deleted.")


# Grab new jobs from a website, Parses JSON code and inserts the data into a list of dictionaries do not need to edit
def fetch_new_jobs():
    query = requests.get("https://remotive.io/api/remote-jobs")
    datas = json.loads(query.text)

    return datas


# Main area of the code. Should not need to edit
def jobhunt(cursor):
    # Fetch jobs from website
    jobpage = fetch_new_jobs()  # Gets API website and holds the json data in it as a list
    # use below print statement to view list in json format
    # print(jobpage)
    add_or_delete_job(jobpage, cursor)


def add_or_delete_job(jobpage, cursor):
    # Add your code here to parse the job page
    for jobdetails in jobpage['jobs']:  # EXTRACTS EACH JOB FROM THE JOB LIST. It errored out until I specified jobs. This is because it needs to look at the jobs dictionary from the API. https://careerkarma.com/blog/python-typeerror-int-object-is-not-iterable/
        # Add in your code here to check if the job already exists in the DB
           existing_jobs = check_if_job_exists(cursor, jobdetails)
       if existing_jobs:  # Job exists, you can handle update if needed
            print(f"Job already exists: {jobdetails['title']}")
        else:  # Job does not exist, add it
            add_new_job(cursor, jobdetails)
            print(f"New job added: {jobdetails['title']}")


# Setup portion of the program. Take arguments and set up the script
# You should not need to edit anything here.
def main():
    # Important, rest are supporting functions
    # Connect to SQL and get cursor
      conn = connect_to_sql()
      cursor = conn.cursor()
      create_tables(cursor)

    while True:  # Infinite Loops. Only way to kill it is to crash or manually crash it. We did this as a background process/passive scraper
            jobhunt(cursor)  
         time.sleep(21600)  # Sleep for 1h, this is ran every hour because API or web interfaces have request limits. Your reqest will get blocked.

               
# Sleep does a rough cycle count, system is not entirely accurate
# If you want to test if script works change time.sleep() to 10 seconds and delete your table in MySQL
if __name__ == '__main__': main()

