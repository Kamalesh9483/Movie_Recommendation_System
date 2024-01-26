import sqlite3
import pandas as pd
# conn = sqlite3.connect('Movie_history.db')
# print("Opened database successfully")

# conn.execute('''CREATE TABLE IF NOT EXISTS MOVIE
#          (userID INT PRIMARY KEY     ,
#          movieInput           TEXT    );''')
# print("Table created successfully")

# conn.close()

def insertData(userID, movieInput):
    conn = sqlite3.connect('Movie_history.db')
    print("Opened database successfully")

    conn.execute('''CREATE TABLE IF NOT EXISTS MOVIE
            (userID INT PRIMARY KEY     ,
            movieInput           TEXT    );''')
    print("Table created successfully")

    conn.execute("INSERT INTO MOVIE (userID,movieInput) \
        VALUES (?, ?)", (userID,movieInput));

    conn.commit()
    print("Records created successfully")
    conn.close()

def displayDB():
    conn = sqlite3.connect('Movie_history.db')
    print("Opened database successfully")
        
    userID = []
    movieInput = []
    cursor = conn.execute("SELECT userID, movieInput from MOVIE")
    # for row in cursor:
    #     print("userID = ", row[0])
    #     userID.append(row[0])
    #     print("movieInput = ", row[1])
    #     movieInput.append(row[1])
    #     print("\n")

    # df = pd.DataFrame(list(zip(userID, movieInput), columns=['userID', 'movieInput']))

    # df = pd.read_sql_table('MOVIE', conn)
    # query = conn.execute("SELECT * FROM MOVIE")
    # cols = [column[0] for column in query.description]
    # results = pd.DataFrame.from_records(cls, data)
    df = pd.read_sql("SELECT * FROM MOVIE", conn)
    print("Operation done successfully")
    return df
    # return (userID,movieInput)
    conn.close()
