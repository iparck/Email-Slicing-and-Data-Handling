import mysql.connector

# Connection details
HOST = "localhost"
USER = "root"
PASSWORD = "1100591029"  # Replace with your actual password
DATABASE = "emailSlicing"

# Connect to the DB
db = mysql.connector.connect(
    host=HOST,
    user=USER,
    password=PASSWORD,
    database=DATABASE
)

mycursor = db.cursor()

# Dummy data
username_list = ["alice", "bob", "charlie", "diana", "eve"]
domain_list = ["gmail", "yahoo", "hotmail", "outlook", "protonmail"]
extension_list = ["com", "com", "com", "com", "ch"]

# Insert function (same logic as in your main code)
def commit_to_db(username_list, domain_list, extension_list):
    n = len(username_list)
    if len(domain_list) != n or len(extension_list) != n:
        print("[ERROR]: Some values are missing")
        return
    
    for i in range(n):
        username = username_list[i]
        domain = domain_list[i]
        extension = extension_list[i]

        sql = "INSERT INTO emails (username, domain, extention) VALUES (%s, %s, %s)"
        values = (username, domain, extension)
        mycursor.execute(sql, values)
    
    db.commit()

# Insert dummy data
commit_to_db(username_list, domain_list, extension_list)

# Optional: Print the inserted data
mycursor.execute("SELECT * FROM emails")
for row in mycursor.fetchall():
    print(row)

# Close connection
db.close()
