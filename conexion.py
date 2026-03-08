import mysql.connector


def obtenerConexion():
    return mysql.connector.connect(host="localhost",
                                   user="root",
                                   port = "3306",
                                   password = "REDACTED",
                                   database="pruebamicaja")

###return mysql.connector.connect(host="localhost",
                                   ##user="micajadb_admin",
                                   ##password = "REDACTED",
                                   ##database="micajaplus")