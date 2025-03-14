import mysql.connector
import streamlit as st
import pandas as pd

# Function to load data from CSV when MySQL fails
def load_data_from_csv():
    try:
        # Attempt to read data from CSV
        df = pd.read_csv('customers.csv')
        return df
    except Exception as e:
        # If CSV loading fails, show an error message and return None
        st.error(f"Failed to load data from CSV: {str(e)}")
        return None

# MySQL connection setup
def connect_to_mysql():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",  # Using TCP/IP instead of localhost
            port="3306",
            user="root",
            passwd="",  # Provide your password if necessary
            db="streamlit_mysql"
        )
        return conn
    except mysql.connector.Error:
        # Catch MySQL connection errors silently
        return None

# Function to fetch all data from MySQL
def view_all_data():
    conn = connect_to_mysql()
    if conn is None:
        # Fallback to CSV if MySQL connection fails
        return load_data_from_csv()
    
    c = conn.cursor()
    c.execute('SELECT * FROM customers ORDER BY id ASC')
    data = c.fetchall()
    conn.close()  # Always close the connection when done

    # Converting the data to a DataFrame with appropriate column names
    columns = [
        "EEID", "Full Name", "JobTitle", "Department", "BusinessUnit", 
        "Gender", "Ethnicity", "Age", "Hire Date", "AnnualSalary", 
        "Bonus", "Country", "City", "id"
    ]
    df = pd.DataFrame(data, columns=columns)
    return df

# Function to fetch all departments from MySQL
def view_all_departments():
    conn = connect_to_mysql()
    if conn is None:
        # Fallback to CSV if MySQL connection fails, silently loading departments from CSV
        return load_data_from_csv()['Department'].unique()  # Assuming 'Department' is a column in the CSV
    
    c = conn.cursor()
    c.execute('SELECT Department FROM customers')
    data = c.fetchall()
    conn.close()  # Always close the connection when done
    return [row[0] for row in data]

# Usage in your Streamlit app
st.title("Customer Data Dashboard")

# Fetch and display all data (fallback to CSV if MySQL fails)
data = view_all_data()
if data is not None:
    st.write(data)

# Fetch and display all departments (fallback to CSV if MySQL fails)
departments = view_all_departments()
if departments is not None:
    st.write(departments)
