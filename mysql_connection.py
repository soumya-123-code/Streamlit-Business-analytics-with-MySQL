import mysql.connector
import streamlit as st
import pandas as pd

# Function to load data from CSV when MySQL fails
def load_data_from_csv():
    try:
        # Attempt to read data from CSV
        df = pd.read_csv('customers.csv')
        st.write("Data loaded from CSV.")
        return df
    except Exception as e:
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
    except mysql.connector.Error as err:
        st.error(f"MySQL connection failed: {err}")
        return None

# Function to fetch all data from MySQL
def view_all_data():
    conn = connect_to_mysql()
    if conn is None:
        # Fallback to CSV if MySQL connection fails
        st.warning("MySQL connection failed, loading data from CSV.")
        return load_data_from_csv()
    
    c = conn.cursor()
    c.execute('SELECT * FROM customers ORDER BY id ASC')
    data = c.fetchall()
    conn.close()  # Always close the connection when done
    return data

# Function to fetch all departments from MySQL
def view_all_departments():
    conn = connect_to_mysql()
    if conn is None:
        # Fallback to CSV if MySQL connection fails
        st.warning("MySQL connection failed, loading departments from CSV.")
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
