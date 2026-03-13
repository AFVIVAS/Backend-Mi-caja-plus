import mysql.connector


def obtenerConexion():
    return mysql.connector.connect(host="localhost",
                                   user="root",
                                   port = 3307,
                                   password = "REDACTED",
                                   database="micajapluss")

###return mysql.connector.connect(host="localhost",
                                   ##user="micajadb_admin",
                                   ##password = "REDACTED",
                                   ##database="micajaplus")