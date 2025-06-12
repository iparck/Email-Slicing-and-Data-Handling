import mysql.connector

HOST = None
USER = None
PASSWORD = None
db = None
mycursor = None
DATABASE = None
TABLE = None



def taking_creds(host, user, password):
    global HOST, USER, PASSWORD
    
    HOST = host
    USER = user
    PASSWORD = password
    
    try:
        test_db = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD
        )
    except Exception as e:
        return str(e)
    test_db.close()
    return True

def setup(database, table):
    global HOST, USER, PASSWORD
    global DATABASE, TABLE, mycursor, db

    DATABASE = database
    TABLE = table

    db = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD
    )

    mycursor = db.cursor()

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
            CREATE TABLE IF NOT EXISTS {TABLE} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(100),
                domain VARCHAR(100),
                extension VARCHAR(100)
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

        sql = f"INSERT INTO {TABLE} (username, domain, extension) VALUES (%s, %s, %s)"
        values = (username, domain, extension)
        mycursor.execute(sql, values)
    
    db.commit()

def get_data():

    global DATABASE, TABLE, mycursor, db

    mycursor.execute(f"SELECT * FROM {TABLE}")
    rows = mycursor.fetchall()
    return rows