import pymysql
import configparser

config = configparser.ConfigParser()
config.read("configurations.ini")

Location    = config["Database Information"]["Location"]
Name        = config["Database Information"]["Name"]
Password    = config["Database Information"]["Password"]
Database    = config["Database Information"]["Database"]
Table       = config["Database Information"]["Table"]


def create_server_connection(): 
    try:
        connection = pymysql.connect(
            host        = Location,
            user        = Name,
            passwd      = Password,
            db          = Database,
            charset     = 'utf8mb4',
            cursorclass = pymysql.cursors.DictCursor
        )
        print("MySQL Database connection successful")
        return connection
    except Exception as e:
        print("There was a problem setting up the connection with the database.\n\t %s" % (e))

def get_headers(server_connection):
    with server_connection.cursor() as cursor:
        cursor.execute(f"DESCRIBE {Table}")
        return cursor.fetchall()    

def get_all(server_connection):
    with server_connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM {Table}")
        return cursor.fetchall()
    
def get_row_count(server_connection):
    with server_connection.cursor() as cursor:
        cursor.execute(f"SELECT COUNT(*) FROM {Table}")
        return cursor.fetchall()