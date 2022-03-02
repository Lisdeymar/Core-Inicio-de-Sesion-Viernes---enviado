from flask import render_template, request, redirect, session
from usuarios_app import app
from usuarios_app.modelos.modelo_dojos import Dojo



@app.route( '/departamentos', methods=["GET"] )
def despliegaDojos():
    listaDojos = Dojo.obtenerListaDojos() #acá llamamos al query y la funcion del modeloDepartamentos "obtenerListaDepartamentos"
    listaDojosConUsuarios = Dojo.obtenerListaDojosConUsuarios()
    print(listaDojosConUsuarios)
    return render_template( "departamentos.html", listaDojos=listaDojos, listaDojosConUsuarios=listaDojosConUsuarios ) 


