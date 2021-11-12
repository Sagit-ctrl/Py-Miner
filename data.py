import sqlite3

def CreateDatabase():
    try:
        sqliteConnection = sqlite3.connect('rank.db')
        cursor = sqliteConnection.cursor()
        sqlite_select_Query = "select sqlite_version();"
        cursor.execute(sqlite_select_Query)
        record = cursor.fetchall()
        cursor.close()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()

def CreateTable():
    try:
        sqliteConnection = sqlite3.connect('rank.db')
        sqlite_create_table_query = '''CREATE TABLE Rank(
                                    id INTEGER PRIMARY KEY,
                                    name TEXT NOT NULL,
                                    point INTEGER NOT NULL ,
                                    time TEXT NOT NULL,
                                    realtime INTEGER NOT NULL);'''

        cursor = sqliteConnection.cursor()
        cursor.execute(sqlite_create_table_query)
        sqliteConnection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Error while creating a sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()

def InsertbyQueryPython(id, name, point, time, realtime):
    try:
        sqliteConnection = sqlite3.connect('rank.db')
        cursor = sqliteConnection.cursor()
        sqlite_insert_with_param = """INSERT INTO Rank
                          (id, name, point, time, realtime) 
                          VALUES (?, ?, ?, ?, ?);"""
        data_tuple = (id, name, point, time, realtime)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqliteConnection.commit()
        print("Insert OK", id)
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()

def readSqliteTable():
    try:
        sqliteConnection = sqlite3.connect('rank.db')
        cursor = sqliteConnection.cursor()
        sqlite_select_query = """SELECT * from Rank"""
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        # print("Total rows are:  ", len(records))
        # print("Printing each row")
        # for row in records:
        #     print("Id: ", row[0])
        #     print("Name: ", row[1])
        #     print("Point: ", row[2])
        #     print("Time: ", row[3])
        #     print("Realtime: ", row[4])
        #     print("\n")
        return records
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()

def updateSqliteTable(name, point):
    try:
        sqliteConnection = sqlite3.connect('rank.db')
        cursor = sqliteConnection.cursor()
        sql_update_query = """Update Rank set point = ? where name = ?"""
        data = (point, name)
        cursor.execute(sql_update_query, data)
        sqliteConnection.commit()
        print("Record Updated successfully")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to update sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()

def deleteSqliteRecord(id):
    try:
        sqliteConnection = sqlite3.connect('rank.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sql_update_query = """DELETE from Rank where id = ?"""
        cursor.execute(sql_update_query, (id,))
        sqliteConnection.commit()
        print("Record deleted successfully")

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to delete reocord from a sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("sqlite connection is closed")

# CreateDatabase()
# CreateTable()
# InsertbyQueryPython(0, 'A', 0, '00:00', 0)
# InsertbyQueryPython(1, 'B', 0, '00:00', 0)
# InsertbyQueryPython(2, 'C', 0, '00:00', 0)
# InsertbyQueryPython(3, 'D', 0, '00:00', 0)
# InsertbyQueryPython(4, 'E', 0, '00:00', 0)