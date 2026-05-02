from flask import Flask, render_template
import psycopg2

app = Flask(__name__)

def conectar():
    conexion = psycopg2.connect(
        host="localhost",
        database="proyecto_crud",
        user="postgres",
        password="BranAkerman456"
    )
    return conexion

@app.route("/")
def inicio():
    try:
        con = conectar()
        con.close()
        return "Conexión exitosa a PostgreSQL "
    except:
        return "Error al conectar"
    
@app.route("/productos")
def productos():
    con = conectar()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM productos")
    datos = cursor.fetchall()
    con.close()

    return render_template("productos.html", productos=datos)


if __name__ == "__main__":
    app.run(debug=True)