import pyodbc
from flask import Flask
global_id = 1


def connect():
    server = 'tcp:mydb5.database.windows.net,1433'
    database = 'myDb'
    username = 'johnny@mydb5'
    password = 'Qwerty123'
    driver = '{ODBC Driver 13 for SQL Server}'
    cnxn = pyodbc.connect('Driver={ODBC Driver 13 for SQL Server};Server=tcp:tstserverdb.database.windows.net,1433;'
                          'Database=test_db;Uid=johnny@tstserverdb;Pwd=Qwerty123;'
                          'Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;TDS_VERSION=8.0')
    return cnxn


def create_table(connection, table_name):
    cursor = connection.cursor()
    with cursor.execute("CREATE TABLE "+str(table_name)+"(PersonID int,LastName varchar(255),FirstName varchar(255),Address varchar(255),City varchar(255) );"):
        print('Successfully created table '+str(table_name))
    connection.commit()


def select(connection, id):
    cursor = connection.cursor()
    cursor.execute("SELECT * from Persons WHERE PersonID=" + id)
    row = cursor.fetchone()
    return row


def insert(connection, lname, fname, address, city):
    cursor = connection.cursor()
    llname = "'"+lname+"'"
    ffname = "'"+fname+"'"
    add = "'"+address+"'"
    town = "'"+city+"'"
    cursor.execute("SELECT MAX(PersonID) FROM Persons")
    row = cursor.fetchone()
    some_id = 1 + int(row[0])
    with cursor.execute("INSERT INTO Persons (PersonID,LastName,FirstName,Address,City) VALUES ("+str(some_id)+","+llname+","+ffname+","+add+","+town+");"):
        print('One row successfully inserted ! ')
    connection.commit()


def delete(connection, id):
    cursor = connection.cursor()
    query = "DELETE FROM Persons WHERE PersonID = ?"
    with cursor.execute(query, id):
        print('Deleted one row!')
    connection.commit()


app = Flask(__name__)

#"CREATE TABLE Persons (PersonID int,LastName varchar(255),FirstName varchar(255),Address varchar(255),City varchar(255) );"
@app.route('/')
def menu():
    conn = connect()
    if conn:
        print("Connection established with database!")
    else:
        print("Internal error !\n")
    #create_table(conn, 'Persons')
    while True:
        print("What you want to do ? \n 1.Select 2.Insert 3.Delete 4.Exit")
        user_input = input("\n")
        if int(user_input) is 1:
            id = input('PersonID: ')
            print(select(conn, id))
        if int(user_input) is 2:
            lName = input('Last name : ')
            fName = input('First name : ')
            address = input('Address : ')
            cityName = input('City : ')
            insert(conn, lName, fName, address, cityName)
        if int(user_input) is 3:
            id = input('PersonID : ')
            delete(conn, id)
        if int(user_input) is 4:
            print('We will exit now')
            return 'Database edit has finised. You should see changes that were made!'
        exit(1)


if __name__ == '__main__':
    app.run()
