import psycopg2

db_host = "devel-db.ctzdh9pwhxzw.us-west-1.rds.amazonaws.com"
db_name = "image_gallery"
db_user = "image_gallery"

password_file = "/mnt/source/.image_gallery_config"
def get_password():
    f = open(password_file, "r")
    result = f.readline()
    f.close()
    return result[:-1]

#function for closing and committing connection
def closeConn():
    conn.commit()

    if(conn):
        cursor.close()
        conn.close()

#function for listing users
def listUsers():
    cursor.execute('SELECT * FROM users;')
    for table in cursor.fetchall():
        print(table)

#function for adding users
def addUser():
    userName = input("Username> ")
    passWord = input("Password> ")
    fullName = input("Full Name> ")
    strExists = "('" + userName + "', '" + passWord + "', '" + fullName + "')" 
    cursor.execute('SELECT * FROM users;')

    try: 
        insertStr = """INSERT INTO users (username, password, full_name) VALUES (%s, %s, %s)"""
        record = (userName, passWord, fullName)
        cursor.execute(insertStr, record)
    except:
        print("Error: user with username " + userName + " already exists")

#function for editing users
def editUser():
    try:  
        userInput = input("Username to edit> ")
        pgSelect = """SELECT * from users where username = %s"""
        cursor.execute(pgSelect, (userInput, ))
        userRecord = cursor.fetchone()
        if userRecord == None:
            print("No such user.")
            return

        passWord = input("New password (press enter to keep current)> ")
        if (passWord != ""):
            pgUpdate = """Update users set password = %s where username = %s"""
            cursor.execute(pgUpdate, (passWord, userInput))

        fullName = input("New full name (press enter to keep current)> ")
        if (fullName != ""):
            pgUpdate = """Update users set full_name = %s where username = %s"""
            cursor.execute(pgUpdate, (fullName, userInput))
    except:
        print("No such user.")

#function for delete user
def deleteUser():
    try:
        userInput = input("Enter username to delete> ")
        confirm = input("Are you sure that you want to delete " + userInput + "? (type yes or leave blank)" )
        confirm.lower()
        if confirm == "yes":
            pgDelete = "DELETE FROM users where username = '" + userInput + "'"
            cursor.execute(pgDelete)
            print("Deleted.")
    except Exception as e:
        print(e)

keepGoing = True
while keepGoing:
    
    conn  = psycopg2.connect(host=db_host, dbname=db_name, user=db_user, password=get_password())
    cursor = conn.cursor()
    txt = input("1) List users\n2) Add user\n3) Edit user\n4) Delete user\n5) Quit\nEnter command> ")


    if txt == "5": 
        print("Bye.")
        keepGoing = False
    elif txt == "1":
        listUsers()
        closeConn()
    elif txt == "2":
        addUser()
        closeConn()
    elif txt == "3":
        editUser()
        closeConn()
    elif txt == "4":
        deleteUser()
        closeConn()
    else:
        print(txt)
    
    

