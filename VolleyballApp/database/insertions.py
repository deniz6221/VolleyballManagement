import mysql.connector
from VolleyballApp.database.database_config import DATABASE_CONFIG

def insertPlayer(values, positions, teams):
    cnx = mysql.connector.connect(**DATABASE_CONFIG)
    cursor = cnx.cursor()
    returnVal = True
    try:
        query = "INSERT INTO Person (username, password, personType) VALUES (%s, %s, 1)"
        values_1 = (values[0], values[1])
        cursor.execute(query, values_1)
        cnx.commit()
        query_2 = "INSERT INTO Player (username, password, name, surname, date_of_birth, height, weight) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query_2, values)
        cnx.commit()
        for i in positions:
            pos_vals = (values[0], i)
            query_3 = "INSERT INTO PlayerPositions (username, position) VALUES (%s, %s)"
            cursor.execute(query_3, pos_vals)
            cnx.commit()
        for i in teams:
            team_vals = (values[0], i)
            query_4 = "INSERT INTO PlayerTeams (username, team) VALUES (%s, %s)"
            cursor.execute(query_4, team_vals)
            cnx.commit()

    except Exception as e:
        print(e)
        cnx.rollback()
        returnVal = False
    finally:
        cursor.close()
        cnx.close()
        return returnVal
    
def insertCoach(values):
    cnx = mysql.connector.connect(**DATABASE_CONFIG)
    cursor = cnx.cursor()
    returnVal = True
    try:
        query = "INSERT INTO Person (username, password, personType) VALUES (%s, %s, 2)"
        values_1 = (values[0], values[1])
        cursor.execute(query, values_1)
        cnx.commit()
        query_2 = "INSERT INTO Coach (username, password, name, surname, nationality) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query_2, values)
        cnx.commit()
    except:
        cnx.rollback()
        returnVal = False
    finally:
        cursor.close()
        cnx.close()
        return returnVal

def insertJury(values):
    cnx = mysql.connector.connect(**DATABASE_CONFIG)
    cursor = cnx.cursor()
    returnVal = True
    try:
        query = "INSERT INTO Person (username, password, personType) VALUES (%s, %s, 3)"
        values_1 = (values[0], values[1])
        cursor.execute(query, values_1)
        cnx.commit()
        query_2 = "INSERT INTO Jury (username, password, name, surname, nationality) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query_2, values)
        cnx.commit()
    except:
        cnx.rollback()
        returnVal = False
    finally:
        cursor.close()
        cnx.close()
        return returnVal

def updateStadium(id, newName):
    cnx = mysql.connector.connect(**DATABASE_CONFIG)
    cursor = cnx.cursor()
    query = "UPDATE Stadium SET stadium_name = %s WHERE stadium_id = %s"
    cursor.execute(query, (newName, id))
    cnx.commit()

    cursor.close()
    cnx.close()

def deleteMatch(id):
    cnx = mysql.connector.connect(**DATABASE_CONFIG)
    cursor = cnx.cursor()
    query = f"DELETE FROM SessionSquads WHERE session_ID = {id}"
    cursor.execute(query)
    cnx.commit()
    query_1 = f"DELETE FROM MatchSession WHERE session_ID = {id}"
    cursor.execute(query_1)
    cnx.commit()
    cursor.close()
    cnx.close()

def rateMatch(id, rating):
    cnx = mysql.connector.connect(**DATABASE_CONFIG)
    cursor = cnx.cursor()
    query = f"UPDATE MatchSession SET rating = {rating} WHERE session_ID = {id}"
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()

def addMatch(values):
    cnx = mysql.connector.connect(**DATABASE_CONFIG)
    cursor = cnx.cursor()
    query = "INSERT INTO MatchSession (session_ID, team_ID, stadium_ID, time_slot, match_date, assigned_jury_username) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(query, values)
    cnx.commit()
    query_2 = f"INSERT INTO SessionSquads (session_ID) VALUES ({values[0]})"
    cursor.execute(query_2)
    cnx.commit()
    cursor.close()
    cnx.close()


def add_session_squad(session_id, u_and_p):
    try:
        cnx = mysql.connector.connect(**DATABASE_CONFIG)
        cursor = cnx.cursor()
        for i in u_and_p:
            query = f"INSERT INTO SessionSquads (played_player_username, session_ID, position_ID) VALUES ('{i['username']}', {session_id}, {i['position']})"
            cursor.execute(query)
            cnx.commit()
        deleteQuery = f"DELETE FROM SessionSquads SS WHERE SS.session_ID = {session_id} AND played_player_username is NULL"
        cursor.execute(deleteQuery)
        cnx.commit()
        cursor.close()
        cnx.close()
        return True
    except:
        cursor.close()
        cnx.close()
        return False
