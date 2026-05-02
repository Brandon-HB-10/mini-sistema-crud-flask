from flask import Flask, render_template, request
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
    

@app.route("/productos")#agrege esta ruta para mostrar los productos
def productos():
    con = conectar()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM productos")
    datos = cursor.fetchall()
    con.close()

    return render_template("productos.html", productos=datos)


@app.route("/agregar_producto", methods=["GET", "POST"])
def agregar_producto():

    if request.method == "POST":
        tipo = request.form["tipo_producto"]
        marca = request.form["marca"]

        print(tipo)
        print(marca)

    return render_template("agregar.html")

if __name__ == "__main__":
    app.run(debug=True)