import mysql.connector
from mysql.connector import Error 

def connect_db():
    db_name = "e_commerce_db"
    user = "root"
    password = "751996Jl"
    host = "localhost"

    try:
        conn = mysql.connector.connect(
            database=db_name,
            user=user,
            password=password,
            host=host
        )

        print("connected to database successfully")
        return conn
    except Error as e:
        print(f"Error: {e}")
        return None
connect_db()