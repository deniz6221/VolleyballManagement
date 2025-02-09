import mysql.connector
from VolleyballApp.database.database_config import DATABASE_CONFIG
from datetime import datetime

def get_positions():
    cnx = mysql.connector.connect(**DATABASE_CONFIG)
    cursor = cnx.cursor()
    query = "SELECT * FROM Positions"
    cursor.execute(query)
    positions = []
    for row in cursor.fetchall():
        positions.append((row[0], row[1]))
    cursor.close()
    cnx.close()
    return tuple(positions)

def get_teams():
    cnx = mysql.connector.connect(**DATABASE_CONFIG)
    cursor = cnx.cursor()
    current_date = datetime.now()
    formatted_date = current_date.strftime("%d.%m.%y")
    print(formatted_date)
    query = "SELECT team_id, team_name FROM Team WHERE STR_TO_DATE(%s, %s) < STR_TO_DATE(contract_finish, %s)"
    cursor.execute(query, (formatted_date, '%d.%m.%Y', '%d.%m.%Y'))
    teams = []
    for row in cursor.fetchall():
        teams.append((row[0], row[1]))
    cursor.close()
    cnx.close()
    return tuple(teams)

def get_stadiums():
    cnx = mysql.connector.connect(**DATABASE_CONFIG)
    cursor = cnx.cursor()
    query = "SELECT * FROM Stadium"
    cursor.execute(query)

    stadiums = []
    for row in cursor.fetchall():
        stadiums.append({"stadium_ID": row[0], "stadium_name": row[1], "stadium_country": row[2]})
    cursor.close()
    cnx.close()
    return stadiums

def get_average_count_rating(username):
    cnx = mysql.connector.connect(**DATABASE_CONFIG)
    cursor = cnx.cursor()
    query = """SELECT MatchCount, AvgRating FROM 
    (SELECT M.assigned_jury_username as username, COUNT(M.assigned_jury_username) as MatchCount
    FROM MatchSession M WHERE M.assigned_jury_username = %s
    GROUP BY M.assigned_jury_username) Q1 INNER JOIN (SELECT M.assigned_jury_username as username, AVG(M.rating) as AvgRating
    FROM MatchSession M WHERE M.assigned_jury_username = %s
    GROUP BY M.assigned_jury_username) Q2 ON Q1.username = Q2.username"""
    cursor.execute(query, (username, username))
    avg_count = [0,0]
    for row in cursor.fetchall():
        avg_count = [row[0], row[1]]
    return avg_count


def get_rateable_matches(username):
    cnx = mysql.connector.connect(**DATABASE_CONFIG)
    cursor = cnx.cursor()
    query = """SELECT M.session_ID, M.match_date FROM MatchSession M
    WHERE M.assigned_jury_username = %s 
    AND M.rating is NULL 
    AND STR_TO_DATE(%s, %s) > STR_TO_DATE(M.match_date, %s)"""
    current_date = datetime.now()
    formatted_date = current_date.strftime("%d.%m.%Y")
    cursor.execute(query, (username, formatted_date, '%d.%m.%Y', '%d.%m.%Y'))
    matches = []
    for row in cursor.fetchall():
        matches.append({"id": row[0], "date": row[1]})
    return matches

def get_average_height(username):
    cnx = mysql.connector.connect(**DATABASE_CONFIG)
    cursor = cnx.cursor()
    query = """SELECT AVG(J2.height) as avg_height FROM (SELECT QFT.username FROM (SELECT MAX(QF.played_count)
    as max_count FROM (SELECT P.username, Count(P.username) as played_count FROM Player P,
    (SELECT played_player_username as username FROM SessionSquads SS,
    (SELECT session_id FROM SessionSquads WHERE played_player_username = %s) Q
    WHERE SS.session_id = Q.session_id) Q1 
    WHERE P.username != %s AND P.username = Q1.username
    GROUP BY P.username) QF) MF, (SELECT P.username, Count(P.username) as player_count FROM Player P,
    (SELECT played_player_username as username FROM SessionSquads SS,
    (SELECT session_id FROM SessionSquads WHERE played_player_username = %s) Q
    WHERE SS.session_id = Q.session_id) Q1 
    WHERE P.username != %s AND P.username = Q1.username
    GROUP BY P.username) QFT WHERE QFT.player_count = MF.max_count) J1 INNER JOIN Player J2 ON J1.username = J2.username"""
    cursor.execute(query, (username, username, username, username))
    avg_height = 0
    for row in cursor.fetchall():
        avg_height = row[0]
    return avg_height

def get_played_players(username):
    cnx = mysql.connector.connect(**DATABASE_CONFIG)
    cursor = cnx.cursor()
    query = "SELECT P.name, P.surname FROM Player P,(SELECT played_player_username as username FROM SessionSquads SS,(SELECT session_id FROM SessionSquads WHERE played_player_username = %s) Q WHERE SS.session_id = Q.session_id) Q1 WHERE P.username != %s AND P.username = Q1.username GROUP BY P.username"
    cursor.execute(query, (username, username))
    players = []
    for row in cursor.fetchall():
        players.append({"name": row[0], "surname": row[1]})
    cursor.close()
    cnx.close()
    return players

def get_match_info(id):
    cnx = mysql.connector.connect(**DATABASE_CONFIG)
    cursor = cnx.cursor()
    query = f"""SELECT Q.session_id,  Q.match_date, T.team_name, S.stadium_name FROM 
            (SELECT * FROM MatchSession WHERE session_id = {id}) Q 
            INNER JOIN Team T ON T.team_id = Q.team_id
            INNER JOIN Stadium S ON S.stadium_id = Q.stadium_id"""
    cursor.execute(query)
    ret = []
    for row in cursor.fetchall():
        ret.append(row[0])
        ret.append(row[1])
        ret.append(row[2])
        ret.append(row[3])
    cursor.close()
    cnx.close()
    return ret

def get_available_time_slots(date):
    cnx = mysql.connector.connect(**DATABASE_CONFIG)
    cursor = cnx.cursor()
    available = [[], [], []]
    for i in range(1,4):
        query = f"""SELECT DISTINCT(S1.stadium_id), S1.stadium_name FROM Stadium S1 WHERE S1.stadium_id NOT IN 
                    (SELECT S.stadium_id FROM 
                    STADIUM S INNER JOIN MatchSession M ON M.stadium_id = S.stadium_id
                    WHERE M.match_date = '{date}' AND (M.time_slot - 1 = {i} OR M.time_slot +1 = {i} OR M.time_slot = {i}) 
                    GROUP BY S.stadium_id)
                    """
        cursor.execute(query)
        for row in cursor.fetchall():
            available[i-1].append(row)
        
    cursor.close()
    cnx.close()    
    return available

def get_juries():
    cnx = mysql.connector.connect(**DATABASE_CONFIG)
    cursor = cnx.cursor()
    juries = []
    query = "SELECT username, name, surname FROM Jury"
    cursor.execute(query)
    for row in cursor.fetchall():
        juries.append({"id": row[0], "name": row[1] + " " + row[2]})
    cursor.close()
    cnx.close()
    return juries

def get_max_match_id():
    cnx = mysql.connector.connect(**DATABASE_CONFIG)
    cursor = cnx.cursor()
    query = "SELECT MAX(session_ID) FROM MatchSession"
    cursor.execute(query)
    for row in cursor.fetchall():
        return row[0]
    cursor.close()
    cnx.close()
    return 1

def get_coach_team_id(username):
    cnx = mysql.connector.connect(**DATABASE_CONFIG)
    cursor = cnx.cursor()
    current_date = datetime.now()
    formatted_date = current_date.strftime("%d.%m.%Y")
    query = f"""SELECT T.team_id, T.team_name FROM Team T WHERE T.coach_username = '{username}' AND 
    (STR_TO_DATE('{formatted_date}', '%d.%m.%Y') < STR_TO_DATE(T.contract_finish, '%d.%m.%Y'))"""
    cursor.execute(query)
    for row in cursor.fetchall():
        return [row[0], row[1]]
    cursor.close()
    cnx.close()
    return []

def get_team_players(team_id):
    cnx = mysql.connector.connect(**DATABASE_CONFIG)
    cursor = cnx.cursor()
    query = f"""SELECT P.username, P.name, P.surname 
    FROM PlayerTeams T INNER JOIN Player P ON P.username = T.username
    WHERE T.team = {team_id}"""
    cursor.execute()
    ret = []
    for row in cursor.fetchall():
        ret.append({"username": row[0], "name": row[1] + " " + row[2]})
    cursor.close()
    cnx.close()
    return ret

def get_player_positions(username):
    cnx = mysql.connector.connect(**DATABASE_CONFIG)
    cursor = cnx.cursor()
    query = f"""SELECT P.position_id, P.position_name 
    FROM Positions P INNER JOIN PlayerPositions PP ON PP.position = P.position_id
    INNER JOIN Player U ON U.username = PP.username
    WHERE U.username = '{username}'
    """
    cursor.execute(query)
    ret = []
    for row in cursor.fetchall():
        ret.append({"position_id": row[0], "position": row[1]})
    cursor.close()
    cnx.close()
    return ret

def get_squad_matches(teamId):
    cnx = mysql.connector.connect(**DATABASE_CONFIG)
    cursor = cnx.cursor()
    query = f"""SELECT M.session_ID, M.match_date, M.time_slot
    FROM MatchSession M , SessionSquads SS
    WHERE M.team_id = {teamId} AND SS.session_ID = M.session_ID 
    AND SS.played_player_username is NULL
    """
    cursor.execute(query)
    ret = []
    for row in cursor.fetchall():
        ret.append({"id": row[0], "date": row[1], "time": row[2]})
    cursor.close()
    cnx.close()
    return ret

def get_available_players(teamID, date, time_slot):
    cnx = mysql.connector.connect(**DATABASE_CONFIG)
    cursor = cnx.cursor()
    query = f"""SELECT P1.username, P1.name, P1.surname FROM Player P1
    INNER JOIN PlayerTeams PT1 ON PT1.username = P1.username
    WHERE P1.username NOT IN
    (SELECT DISTINCT(P.username)
    FROM Player P INNER JOIN PlayerTeams PT ON P.username = PT.username
    INNER JOIN SessionSquads SS ON SS.played_player_username = P.username
    INNER JOIN MatchSession M ON M.session_ID = SS.session_ID
    WHERE PT.team = {teamID} AND M.match_date = '{date}'
    AND (M.time_slot = {time_slot} OR M.time_slot = {time_slot+1} OR M.time_slot = {time_slot-1}))
    AND PT1.team = {teamID}
    """
    cursor.execute(query)
    ret = []
    for row in cursor.fetchall():
        ret.append({"username": row[0], "name": row[1] + " " + row[2], "positions": get_player_positions(row[0])})
    cursor.close()
    cnx.close()
    return ret