import pymysql
from dotenv import load_dotenv  # variables de entorno 
import os
from flask import Flask, jsonify, request,render_template
from flask_cors import CORS

#Cargar Variables de entorno
load_dotenv()

app = Flask(__name__)
CORS(app) #para acceder al servicio desde cualquir dominio
#eviat error Acces-control-Alow-Otigin

#Definir parámetros de conexión al servidor
conf =  {
    "host":os.getenv("HOST"),          #nombre del sv
    "user":os.getenv("USER"),
    "password":os.getenv("PASSWORD_DB"),
    "cursorclass":pymysql.cursors.DictCursor,
    "database":os.getenv("DATABASE")
}

@app.route('/')
def index():
    return render_template('index.html')

#Login POST
@app.route('/inicipyarsesion',methods=['POST'])
def iniciarSesion():
    usuario=request.form["usuario"]
    clave=request.form["clave"]
    conn = pymysql.connect(**conf)
    cursor=conn.cursor()
    cursor.execute("select * from investigadores where usuario= %s", (usuario))

    rows = cursor.fetchall()
    if len(rows) == 1:
        for i in rows:
            if i.get('clave')==clave:
                respuesta = jsonify(rows)
            else:
                respuesta="-2"
    else:
        respuesta="-1"
    
    cursor.close()
    conn.close()
    return respuesta

@app.route('/actoresinsert',methods=['POST'])
def actoresinsert():
    #idcategoria  diferente form["idcategoria"]
    #Leyendo variables de formulario q recibe el servicio
    actor=request.form["actors"]
    tipoactor=request.form["tipoactors"]
    actoperativa=request.form["actoperativas"]
    distrito=request.form["distritos"]
    cp_nombre=request.form["cpoblados"]
    conn = pymysql.connect(**conf)    
    cursor = conn.cursor() 
    print("valores",actor,tipoactor,actoperativa,distrito,cp_nombre)    	
    #cursor.execute('Insert into actorentidad(ActorEntidad_Nom,TipoActor_idTipoActor,ActOperativa_idActOperativa,Distrito_idDistrito,cp_nombre) values (%s,%s,%s,%s,%s)', (actor,tipoactor,actoperativa,distrito,cp_nombre))
    cursor.execute("Insert into actorentidad( `ActorEntidad_Nom`, `TipoActor_idTipoActor`, `ActOperativa_idActOperativa`, `Distrito_idDistrito`, `CPoblado_idCPoblado`) values(%s,%s,%s,%s,%s)", (actor,tipoactor,actoperativa,distrito,cp_nombre))
    idActorEntidad = cursor.lastrowid
    cursor.close()
    conn.close()
    if idActorEntidad:
        return jsonify(idActorEntidad)
    else: 
        return jsonify(0)

#Guardar POST
@app.route('/actoresupdate',methods=['POST'])
def investigadoresupdate():
    #Leyendo variables de formulario q recibe el servicio
    idcliente=request.form["idcliente"]
    usuario=request.form["usuario"]
    nombres=request.form["nombres"]
    correo=request.form["correo"]
    orcid=request.form["orcid"]
    ctivitae=request.form["ctivitae"]
    cargo=request.form["cargo"]
    direccion=request.form["direccion"]
    ciudad=request.form["ciudad"]
    region=request.form["region"]
    pais=request.form["pais"]
    telefono=request.form["telefono"]


    conn = pymysql.connect(**conf)
    cursor=conn.cursor()
    cursor.execute("update investigadores set usuario= %s,nombres= %s,correo= %s,orcid= %s,ctivitae= %s,cargo= %s,direccion= %s,ciudad= %s,region= %s,pais = %s,telefono= %s where idcliente = %s", (usuario,nombres,correo,orcid,ctivitae,cargo,direccion,ciudad,region,pais,telefono,idcliente))
    cursor.close()
    conn.close()
    return idcliente

#Eliminar POST
@app.route('/investigadoresdelete',methods=['POST'])
def investigadoresdelete():
    #Leyendo variables de formulario q recibe el servicio
    idcliente=request.form["idcliente"]
    conn = pymysql.connect(**conf)
    cursor=conn.cursor()
    cursor.execute("delete from investigadores where idcliente = %s", (idcliente))
    cursor.close()
    conn.close()
    return idcliente


@app.route('/actores')
def actores():
    try:
        conn = pymysql.connect(**conf)
        cursor=conn.cursor()
        cursor.execute("select * from vista_actorentida")
        rows=cursor.fetchall()
        resp=jsonify(rows)
        cursor.close()
        return resp
        conn.close()
        print("connection closed successfully")
    except pymysql.Error as e:
        print("could not close connection error pymysql %d: %s" %(e.args[0], e.args[1]))

@app.route('/oficina')
def oficina():
    conn = pymysql.connect(**conf)
    cursor=conn.cursor()
    cursor.execute("select * from oficina")
    rows=cursor.fetchall()
    resp=jsonify(rows)
    cursor.close()
    conn.close()
    return resp

@app.route('/oficina/<int:id>')
def oficinas(id):
    conn = pymysql.connect(**conf)
    cursor=conn.cursor()
    cursor.execute("select * from actoperativa where oficina_i_id_oficina = %s",id)
    rows=cursor.fetchall()
    resp=jsonify(rows)
    cursor.close()
    conn.close()
    return resp


@app.route('/colaborador/<int:id>')
def colaborador(id):
    conn = pymysql.connect(**conf)
    cursor=conn.cursor()
    cursor.execute("select * from vistarespoficusuario where i_id_oficina = %s",id)
    rows=cursor.fetchall()
    resp=jsonify(rows)
    cursor.close()
    conn.close()
    return resp

@app.route('/tipoactor')
def tipoactor():
    conn = pymysql.connect(**conf)
    cursor=conn.cursor()
    cursor.execute("select * from tipoactor")
    rows=cursor.fetchall()
    resp=jsonify(rows)
    cursor.close()
    conn.close()
    return resp


@app.route('/departamento')
def departamento():
    conn = pymysql.connect(**conf)
    cursor=conn.cursor()
    cursor.execute("select * from departamento")
    rows=cursor.fetchall()
    resp=jsonify(rows)
    cursor.close()
    conn.close()
    return resp

@app.route('/provincia/<int:id>')
def provincia(id):
    conn = pymysql.connect(**conf)
    cursor=conn.cursor()
    cursor.execute("select * from provincia where Departamento_idDepartamento = %s",id)
    rows=cursor.fetchall()
    resp=jsonify(rows)
    cursor.close()
    conn.close()
    return resp

@app.route('/distrito/<int:id>')
def distrito(id):
    conn = pymysql.connect(**conf)
    cursor=conn.cursor()
    cursor.execute("select * from distrito where Provincia_idProvincia = %s",id)
    rows=cursor.fetchall()
    resp=jsonify(rows)
    cursor.close()
    conn.close()
    return resp


@app.route('/cpoblado/<int:id>')
def cpoblado(id):
    conn = pymysql.connect(**conf)
    cursor=conn.cursor()
    cursor.execute("select * from cpoblado where Distrito_idDistrito = %s",id)
    rows=cursor.fetchall()
    resp=jsonify(rows)
    cursor.close()
    conn.close()
    return resp

#Eliminar POST
@app.route('/actordelete',methods=['POST'])
def actordelete():
    #Leyendo variables de formulario q recibe el servicio
    idActorEntidad=request.form["idActorEntidad"]
    conn = pymysql.connect(**conf)
    cursor=conn.cursor()
    cursor.execute("delete from actorentidad where idActorEntidad = %s", (idActorEntidad))
    cursor.close()
    conn.close()
    return idActorEntidad


if __name__ == "__main__":
    app.run(debug=True)

