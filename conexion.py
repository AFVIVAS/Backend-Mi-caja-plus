import mysql.connector

def obtenerConexion():
    return mysql.connector.connect(host="localhost",
                                   user="root",
                                   password = "REDACTED",
                                   database="micajaplus")

###return mysql.connector.connect(host="localhost",
                                   ##user="micajadb_admin",
                                   ##password = "REDACTED",
                                   ##database="micajaplus")