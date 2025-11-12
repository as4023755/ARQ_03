import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",  
        password="as4023755",  # replace with your MySQL password
        database="bus_reservation"
    )
