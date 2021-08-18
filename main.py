from flask import Flask,render_template, request,url_for, redirect
from flaskext.mysql import MySQL
app = Flask(__name__, static_url_path="/static")
mysql = MySQL()
app.config["MYSQL_DATABASE_HOST"] = "127.0.0.1"
app.config["MYSQL_DATABASE_USER"] = "root"
app.config["MYSQL_DATABASE_PASSWORD"] = ""
app.config["MYSQL_DATABASE_DB"] = "Nuevo"
app.config["MYSQL_DATABASE_PORT"] = 3306
mysql.init_app(app)

@app.route("/")

def index():

  return render_template("index.html")

@app.route("/rejilla")
def rejilla_html():
     return render_template('html_rejilla.html')
@app.route("/index")
def index_html():
    return render_template("/index.html")

@app.route("/Formulario")
def Formulario_html():

    #conn = mysql.connect()
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM datos")

    datos = cursor.fetchall()

    print(datos)
    cursor.close()

    return render_template("Formulario.html", producto=datos)

@app.route("/guardar_producto", methods=["POST"])
def guardar_producto():
     Nombre = request.form["Nombre"]
     Pelicula = request.form["Pelicula"]
     Correo = request.form["Correo"]
     Opinion = request.form["Opinion"]

     #abrimos conexion
     conn = mysql.connect()
     #crear una interacion a la conexion a la bd
     cursor = conn.cursor()

     cursor.execute("INSERT INTO datos(Nombre, Pelicula, Correo, Opinion) VALUES (%s,%s,%s,%s)", (Nombre, Pelicula, Correo, Opinion))

     #return Nombre + " " + Pelicula + " " + Correo + " " + Opinion

     # Actualizar la conexion
     conn.commit()
     # Cerramos la interacion y limpia la conexion para que quede vacia
     cursor.close()

     return redirect("/Formulario")

@app.route("/eliminar_producto/<string:id>")
def eliminar_producto(id):
    conn = mysql.connect()
    cursor = conn.cursor()

    #cursor.execute("DELETE FROM datos where id={0}".format(id))
    cursor.execute("DELETE FROM `datos`")
    conn.commit()
    cursor.close()

    #return "Dato eliminado "+id
    return redirect("/Formulario")

@app.route("/consulta_producto/<id>")
def obtener_producto(id):
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("Select * From datos")
    dato=cursor.fetchone()
    print(dato)
    cursor.close()
    return render_template("form_editar_producto.html", producto=dato)

@app.route("/editar_producto/<id>", methods=['POST'])
def editar_producto(id):
    Nombre = request.form["Nombre"]
    Pelicula = request.form["Pelicula"]
    Correo = request.form["Correo"]
    Opinion = request.form["Opinion"]

    conn = mysql.connect()
    cursor = conn.cursor()
    #cursor.execute("UPDATE datos SET Nombre=%s, Pelicula=%s, Correo=%s, Opinion=%, WHERE id=%s", (Nombre, Pelicula, Correo, Opinion))
    cursor.execute("UPDATE datos SET Nombre=%s",(Nombre))

    conn.commit()
    cursor.close()

    return redirect("/Formulario")

if __name__ == '__main__':
 app.run(port=8000,debug=True)