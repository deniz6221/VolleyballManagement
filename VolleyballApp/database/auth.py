import mysql.connector
from VolleyballApp.database.database_config import DATABASE_CONFIG

def check_session_key(request):
    if not request.session.has_key("username") or not request.session.has_key("password"):
        return False
    return True

def loginAuth(username, password):
    cnx = mysql.connector.connect(**DATABASE_CONFIG)
    cursor = cnx.cursor()
    query = f"SELECT * FROM Person P WHERE P.username= '{username}' AND P.password = '{password}' "
    cursor.execute(query)
    if cursor is None:
        cursor.close()
        cnx.close()
        return -1
    for row in cursor:
        return row[2]
    cursor.close()
    cnx.close()
