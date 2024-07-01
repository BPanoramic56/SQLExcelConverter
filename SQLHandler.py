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

def ensure_table_existence(server_connection, TableName):
    with server_connection.cursor() as cursor:
        cursor.execute(f"SELECT COUNT(*) FROM  information_schema.tables WHERE table_schema = '{Database}' AND table_name = '{TableName}';")
        return (cursor.fetchall()[0]['COUNT(*)']) > 0
    
def create_table(server_connection, TableName, TableColumns):
    columns = []
    for name in TableColumns:
        columns.append(f"{name} VARCHAR(255)")
    columns_formatted = ", ".join(columns)
    print(f"CREATE TABLE {TableName} ({columns_formatted});")
    with server_connection.cursor() as cursor:
        query = f"CREATE TABLE {TableName} ({columns_formatted});"
        cursor.execute(query)
    server_connection.commit()

def add_row(server_connection, table_name, value_list):
    print(f"INSERT INTO {table_name} VALUES {value_list});")
    columns_formatted = f", ".join([f'"{element}"' for element in value_list])
    print(f"INSERT INTO {table_name} VALUES ({columns_formatted});")
    with server_connection.cursor() as cursor:
        query = f"INSERT INTO {table_name} VALUES ({columns_formatted});"
        cursor.execute(query)
    server_connection.commit()