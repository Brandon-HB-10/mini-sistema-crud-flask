from flask import Flask, render_template, request, redirect
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
        estatus = request.form["estatus"]
        fecha = request.form["fecha"]
        cantidad = request.form["cantidad"]
        precio = request.form["precio"]


        con = conectar()
        cursor = con.cursor()

        cursor.execute("INSERT INTO productos (tipo_producto, marca, estatus, fecha_entrega, cantidad, precio_compra) " \
        "VALUES (%s, %s, %s, %s, %s, %s)",(tipo, marca, estatus, fecha, cantidad, precio))

        con.commit()
        con.close()

        return redirect("/productos")

    return render_template("agregar.html")

if __name__ == "__main__":
    app.run(debug=True)