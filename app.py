from flask import Flask
import psycopg2

crud_m = Flask(__name__)

def conectar():
    conexion = psycopg2.connect(
        host="localhost",
        database="proyecto_crud",
        user="postgres",
        password="BranAkerman456"
    )
    return conexion

@crud_m.route("/")
def inicio():
    try:
        con = conectar()
        con.close()
        return "Conexión exitosa a PostgreSQL "
    except:
        return "Error al conectar"

if __name__ == "__main__":
    crud_m.run(debug=True)