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

#table = """
#    CREATE TABLE users (
#        user_id SERIAL PRIMARY KEY,
#        user_name VARCHAR(50) NOT NULL
#        )
#    """
insert = """
    INSERT INTO users(username, password, full_name)
    VALUES('jon', 'password', 'jonkoh');
    """


conn  = psycopg2.connect(host=db_host, dbname=db_name, user=db_user, password=get_password())
cursor = conn.cursor()
#cursor.execute(table)
cursor.execute(insert)
cursor.execute('SELECT * from users;')
for row in cursor:
    print(row)

cursor.close()
conn.commit()

