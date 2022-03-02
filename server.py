#from flask import Flask
from usuarios_app import app
from usuarios_app.controladores import controlador_dojos, controlador_usuarios

#from carpetageneral.carpetaControladores import archivocontroladorNombreTabla.py
#si hay más controladores colocar una coma , y el nombre del archivo controlador, o se puede 
#hacer una linea por cada controlador ejem:
#from usuarios_app.controladores import controlador_usuarios
if __name__ == "__main__":
    app.run( debug = True )