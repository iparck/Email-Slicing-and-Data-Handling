import mysql
import mysql.connector

HOST = input("Enter host name - ")
USER = input("Enter user name - ")
PASSWORD = input("Enter your SQL password - ")

db = mysql.connector.connect(
    host=HOST,
    user=USER,
    password=PASSWORD
)

mycursor = db.cursor()

DATABASE = None
TABLE = None

def setup(database, table):

    global DATABASE, TABLE, mycursor, db

    DATABASE = database
    TABLE = table


    mycursor.execute(f"CREATE DATABASE IF NOT EXISTS {database};")
    db.close()

    db = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=database
    )

    mycursor = db.cursor()

    mycursor.execute(
        f"""
            CREATE TABLE IF NOT EXISTS {table} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(100),
                domain VARCHAR(100),
                extention VARCHAR(100)
            )
        """
    )


def commit_to_db(username_list, domain_list, extension_list):

    global DATABASE, TABLE, mycursor, db

    n = len(username_list)
    if len(domain_list) != n or len(extension_list) != n:
        return "[ERROR]: Some values are missing"
    
    for i in range (0,n):
        username = username_list[i]
        domain = domain_list[i]
        extension = extension_list[i]

        sql = f"INSERT INTO {TABLE} (username, domain, extention) VALUES (%s, %s, %s)"
        values = (username, domain, extension)
        mycursor.execute(sql, values)
    
    db.commit()

def get_data():

    global DATABASE, TABLE, mycursor, db

    mycursor.execute(f"SELECT * FROM {TABLE}")
    rows = mycursor.fetchall()
    return rows