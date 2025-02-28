## Lidsyda NOuanphachan
## Class CNE340 Winter 2025

import mysql.connector
import time
#import json
import requests
#from datetime import date
#import html2text


# Connect to database
# You may need to edit the connect function based on your local settings.#I made a password for my database because it is important to do so. Also make sure MySQL server is running or it will not connect
def connect_to_sql():
    conn = mysql.connector.connect(user='root', password='',
                                   host='127.0.0.1', database='cne340')
    return conn


# Create the table structure
def create_tables(conn, cursor):  # ✅ Pass 'conn' as a parameter
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INT PRIMARY KEY AUTO_INCREMENT,
            Job_id VARCHAR(50) NOT NULL UNIQUE,
            company VARCHAR(300),
            Created_at DATE,
            url VARCHAR(2000),
            Title TEXT,
            Description TEXT
        );
    """)
    conn.commit()   # Ensure changes are saved

# Query the database.
# You should not need to edit anything in this function
def query_sql(cursor, query):
    cursor.execute(query)
    return cursor


# Add a new job
def add_new_job(cursor, job_details):
    """Insert a new job into the jobs table."""
    if 'title' in job_details and 'description' in job_details:
        cursor.execute("INSERT INTO jobs(Title, Description) VALUES(%s, %s)",
                       (job_details['title'], job_details['description']))
    else:
        print(f"Job missing required data: {job_details}")

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
    try:
        query = requests.get("https://remotive.io/api/remote-jobs")
        query.raise_for_status()
        datas = query.json()
        return datas.get('jobs', [])  # Return empty list if 'jobs' is missing
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return []

# Main area of the code. Should not need to edit
def jobhunt(cursor):
    # Fetch jobs from website
    jobpage = fetch_new_jobs()  # Gets API website and holds the json data in it as a list
    # use below print statement to view list in json format
    # print(jobpage)
    add_or_delete_job(jobpage, cursor)


def add_or_delete_job(jobpage, cursor):
    for jobdetails in jobpage:
        existing_jobs = check_if_job_exists(cursor, jobdetails)

        if existing_jobs:
            print(f"Job already exists: {jobdetails['title']}")
        else:
            if 'id' in jobdetails and jobdetails['id'].strip():  # Ensure Job_id is valid
                job_details = {'id': jobdetails['id'], 'title': jobdetails['title'], 'description': jobdetails['description']}
                add_new_job(cursor, job_details)
                print(f"New job added: {jobdetails['title']}")
            else:
                print(f"Skipping job due to missing Job_id: {jobdetails}")

def update_job(cursor, jobdetails):
    cursor.execute("""
        UPDATE jobs SET Title = %s, Description = %s WHERE Job_id = %s
    """, (jobdetails['title'], jobdetails['description'], jobdetails['id']))
    cursor.connection.commit()
    print(f"Job updated: {jobdetails['title']}")
    jobdetails = {
        'id': '12345',
        'title': 'Software Engineer',
        'company': 'Tech Corp',
        'description': 'A software engineering role at Tech Corp',
        'url': 'https://techcorp.com/jobs/12345'
    }

# Setup portion of the program. Take arguments and set up the script
# You should not need to edit anything here.
def main():
    import mysql.connector
    # Important, rest are supporting functions
    # Connect to SQL and get cursor
    conn = connect_to_sql()
    cursor = conn.cursor()
    create_tables(conn,cursor)


    while True:  # Infinite Loops. Only way to kill it is to crash or manually crash it. We did this as a background process/passive scraper
        jobhunt(cursor)
        time.sleep(21600)

# Sleep does a rough cycle count, system is not entirely accurate
# If you want to test if script works change time.sleep() to 10 seconds and delete your table in MySQL
if __name__ == '__main__': main()

