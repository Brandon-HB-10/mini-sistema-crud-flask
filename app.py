from flask import Flask, render_template, request, redirect, session
import psycopg2

app = Flask(__name__)
app.secret_key = "clave_super_secreta"

def conectar():
    conexion = psycopg2.connect(
        host="localhost",
        database="proyecto_crud",
        user="postgres",
        password="BranAkerman456"
    )
    return conexion

#funion para asegurar los enlaces del crud y que solo el usuario registrado pueda acceder a ellos.
from functools import wraps

def login_requerido(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "usuario" not in session:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated
    
@app.route("/")
@login_requerido
def inicio():

    return render_template("inicio.html")


#agrege suta del login para que solo el usuario registrado en la bd pueda entrar a la pagina principal.
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        usuario = request.form["usuario"]
        password = request.form["password"]

        con = conectar()
        cursor = con.cursor()

        cursor.execute(
            "SELECT * FROM usuarios WHERE usuario=%s AND password=%s",
            (usuario, password)
        )

        usuario_encontrado = cursor.fetchone()

        con.close()

        if usuario_encontrado:
            session["usuario"] = usuario
            return redirect("/")

        else:
            return render_template("login.html", error="Datos incorrectos")

    return render_template("login.html")


#ruta de cerrar secion.
@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect("/login")


@app.route("/productos")#agrege esta ruta para mostrar los productos
@login_requerido
def productos():
    

    con = conectar()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM productos ORDER BY id ASC")
    datos = cursor.fetchall()
    con.close()

    

    return render_template("productos.html", productos=datos)




@app.route("/agregar_producto", methods=["GET", "POST"])
@login_requerido
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


@app.route("/editar_producto/<int:id>", methods=["GET", "POST"])
@login_requerido
def editar_producto(id):
    
    if request.method == "POST":
        tipo = request.form["tipo_producto"]
        marca = request.form["marca"]
        estatus = request.form["estatus"]
        fecha = request.form["fecha"]
        cantidad = request.form["cantidad"]
        precio = request.form["precio"]
        
        con = conectar()
        cursor = con.cursor()

        cursor.execute("UPDATE productos SET tipo_producto=%s," \
        " marca=%s, estatus=%s, fecha_entrega=%s, cantidad=%s," \
        " precio_compra=%s WHERE id=%s",(tipo, marca, estatus, fecha, cantidad, precio, id))

        con.commit()
        con.close()

        return redirect("/productos")

    con = conectar()
    cursor = con.cursor()

    cursor.execute("SELECT * FROM productos WHERE id = %s", (id,))
    producto = cursor.fetchone()

    con.close()

    return render_template("editar.html", producto=producto)

@app.route("/eliminar_producto/<int:id>")
@login_requerido
def eliminar_producto(id):

    con = conectar()
    cursor = con.cursor()

    cursor.execute("DELETE FROM productos WHERE id = %s", (id,))

    con.commit()
    con.close()

    return redirect("/productos")

#Agregamos los mismo pero para Clientes :-----------

@app.route("/clientes")
@login_requerido
def clientes():
    con = conectar()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM clientes ORDER BY id ASC")
    datos = cursor.fetchall()
    con.close()
    return render_template("clientes.html", clientes=datos)


@app.route("/agregar_cliente", methods=["GET", "POST"])
@login_requerido
def agregar_cliente():
    if request.method == "POST":
        nombre = request.form["nombre"]
        telefono = request.form["telefono"]
        correo = request.form["correo"]
        direccion = request.form["direccion"]

        con = conectar()
        cursor = con.cursor()
        cursor.execute("INSERT INTO clientes (nombre, telefono, correo, direccion) "
                       "VALUES (%s, %s, %s, %s)", (nombre, telefono, correo, direccion))
        con.commit()
        con.close()
        return redirect("/clientes")

    return render_template("agregar_cliente.html")


@app.route("/editar_cliente/<int:id>", methods=["GET", "POST"])
@login_requerido
def editar_cliente(id):
    if request.method == "POST":
        nombre = request.form["nombre"]
        telefono = request.form["telefono"]
        correo = request.form["correo"]
        direccion = request.form["direccion"]

        con = conectar()
        cursor = con.cursor()
        cursor.execute("UPDATE clientes SET nombre=%s, telefono=%s, correo=%s, direccion=%s "
                       "WHERE id=%s", (nombre, telefono, correo, direccion, id))
        con.commit()
        con.close()
        return redirect("/clientes")

    con = conectar()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM clientes WHERE id = %s", (id,))
    cliente = cursor.fetchone()
    con.close()
    return render_template("editar_cliente.html", cliente=cliente)


@app.route("/eliminar_cliente/<int:id>")
@login_requerido
def eliminar_cliente(id):
    con = conectar()
    cursor = con.cursor()
    cursor.execute("DELETE FROM clientes WHERE id = %s", (id,))
    con.commit()
    con.close()
    return redirect("/clientes")


@app.route("/ayuda")
@login_requerido
def ayuda():
    return render_template("ayuda.html")



if __name__ == "__main__":
    app.run(debug=True)