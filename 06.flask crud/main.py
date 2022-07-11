
from flask import Flask, render_template, request, redirect, flash,session
import controlador_juegos
from bd import obtener_conexion

app = Flask(__name__)
#app.secret_key = b'\xaa\xe4V}y~\x84G\xb5\x95\xa0\xe0\x96\xca\xa7\xe7'
app.secret_key = "esta es la clve secreta"
"""
Definición de rutas
"""


@app.route("/agregar_juego")
def formulario_agregar_juego():
    return render_template("agregar_juego.html")


@app.route("/guardar_juego", methods=["POST"])
def guardar_juego():
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]
    controlador_juegos.insertar_juego(nombre, descripcion, precio)
    # De cualquier modo, y si todo fue bien, redireccionar
    return redirect("/juegos")


@app.route("/")
@app.route("/juegos")
def juegos():
    juegos = controlador_juegos.obtener_juegos()
    return render_template("juegos.html", juegos=juegos)


@app.route("/eliminar_juego", methods=["POST"])
def eliminar_juego():
    controlador_juegos.eliminar_juego(request.form["id"])
    return redirect("/juegos")


@app.route("/formulario_editar_juego/<int:id>")
def editar_juego(id):
    # Obtener el juego por ID
    juego = controlador_juegos.obtener_juego_por_id(id)
    return render_template("editar_juego.html", juego=juego)


@app.route("/actualizar_juego", methods=["POST"])
def actualizar_juego():
    id = request.form["id"]
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]
    controlador_juegos.actualizar_juego(nombre, descripcion, precio, id)
    return redirect("/juegos")


def valid_login(usuario,pws):

    conexion = obtener_conexion()
   
    sql  = "SELECT id, usuario, nombres FROM usuarios WHERE usuario = %s AND pws = %s"
    dsUser = None
    with conexion.cursor() as cursor:
        cursor.execute(sql, (usuario,pws))
        dsUser = cursor.fetchone()
    conexion.close()
    return dsUser

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['usuario'],
                       request.form['pws']):
            session["usuario"] = request.form['usuario']
            session["logged"] = True

            return redirect("/juegos")
        else:
            error = 'Invalid username/password'
            
    session["logged"] = False
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', error=error)


@app.route("/logout")
def logout():
    session.pop("usuario", None)
    session.pop("logged", None)
    return redirect("/login")

# Iniciar el servidor
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
