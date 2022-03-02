from flask import render_template, request, redirect, session, flash
from usuarios_app import app
from usuarios_app.modelos.modelo_usuarios import Usuario
from usuarios_app.modelos.modelo_dojos import Dojo #importamos Dojo para jalar el nombre de los dojos y utilizarlo en Ruta 1A Registro y en 2C Editar
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

#RUTA 1, la ruta del index
@app.route( '/', methods=['GET'] )
def despliegaRegistroLogin():
    return render_template( "index.html", listaDojos = Dojo.obtenerListaDojos() )


#Ruta 1A POST Registrar, insertas información y click, redirecciona a ruta 2
# "y" Se hace cambios para permitir que el usuario se registre con su departamento
@app.route( '/registroUsuario', methods=["POST"] )
def registrarUsuario(): #Dicc que se va a mandar al query mismos atributos que insert en el form Registro
    if not Usuario.validarRegistro(request.form):
        return redirect('/')
    passwordEncriptado = bcrypt.generate_password_hash( request.form["password"] ) ##ENCRIPTACION 1.3: dentro de los () pongo el request.form password, defino la variable y lo colco en el dicc
    nuevoUsuario = {
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"], 
        "password" : passwordEncriptado, ##ENCRIPTACION 1.4
        "dojo_id" : request.form["dojo_id"] #dojo_id colocamos el mismo atributo que en la Tabla usuarios.
    }
    session["first_name"] = request.form["first_name"] #lo de la sesion para verificacion
    session["last_name"] = request.form["last_name"] #lo de la sesion para verificacion
    resultado = Usuario.agregaUsuario( nuevoUsuario )
    if type( resultado ) is int and resultado == 0:
        return redirect( '/dashboard' )


#Ruta 1B POST Login, insertas información y click, redirecciona a ruta 2
# x No necesita mingun cambio
@app.route( '/login', methods=["POST"] )
def loginUsuario():
    loginUsuario = request.form["loginUsuario"] #la denominacion lo utilizamos en el login template index
    passwordUsuario = request.form["passwordUsuario"] ##ENCRIPTACION 1.5: eliminamos passwordUsuario del diccionario de abajo

    usuario = {
        "email" : loginUsuario ##ENCRIPTACION 1.6: eliminamos passwordUsuario de este diccionario
    }
    resultado = Usuario.verificaUsuario( usuario )

    if resultado == None:
        flash( "El nombre de usuario está escrito incorrectamente", "login" ) #FLASH VALIDACION %%%%%%%%%%
        return redirect( '/' )
    else:
        if not bcrypt.check_password_hash( resultado.password, passwordUsuario ): ##ENCRIPTACION 1.7-MODELOU IR: en el login colocamos el password por eso encriptamos
            flash( "El password es incorrecto", "login" ) #FLASH VALIDACION %%%%%%%%%%
            return redirect( '/' )
        else:
            session["first_name"] = resultado.first_name
            session["last_name"] = resultado.last_name
            return redirect( '/dashboard' )

#if not bcrypt.check_password_hash( resultado.password[0], passwordUsuario ): 

#---------------------------------------------------------------------------
#RUTA 2 despliega dashboard, portal usuario GET

@app.route( '/dashboard', methods=["GET"] )
def despliegaDashboard():
    if 'first_name' in session:
        listaUsuarios = Usuario.obtenerListaUsuarios()
        return render_template( "dashboard.html", usuarios=listaUsuarios )
        #"usuarios" hace referencia al template dashboard cómo será denominado allí la lista
    else:
        return redirect( '/' ) 


#Ruta 2A boton Logout (GET), click y redirecciona a Ruta 1
# x No necesita mingun cambio
@app.route( '/logout', methods=["GET"] )
def logoutUsuario():
    session.clear()
    return redirect( '/' )


#Ruta 2B boton Eliminar (POST), click, elimina y redirecciona a Ruta 2
# x No necesita mingun cambio
@app.route( '/usuario/remover/<int:id>', methods=["POST"] )
def eliminarUsuario( id ):
    print( id )
    usuarioAEliminar = {
        "id": id
    }
    resultado = Usuario.eliminarUsuario( usuarioAEliminar )
    print( resultado ) #print
    return redirect( '/dashboard' )


#Ruta 2C boton Editar (GET), no se añade informacion por eso es GET, click y 
# renderiza a Ruta 3 template, antes de renderizarlo vamos a jalar los datos del id 
# en el modelo-

# "y" Vamos a permitir al usuario cambiar de departamento, por eso añadimos departamento en el html de editar
# esto es solo el boton despliega así que nos vamos a la Ruta 3A donde es la edicion
@app.route( '/usuario/editar/<int:id>', methods=["GET"] )
def despliegaEditar( id ):
    usuarioAEditar = {
        "id": id
    }
    resultado = Usuario.obtenerDatosUsuario( usuarioAEditar )
    return render_template( "editarUsuario.html", usuario=resultado[0], listaDojos = Dojo.obtenerListaDojos() ) #Importamos dojos y llamamos a la listaDojos 
        #y la funcion del controlador y modeloDojos para poder editar ) 
        # #para el placeholder[0]

#ahora vamos a crear el template en html, editarUsuario.html
#---------------------------------------------------------------------------

#Ruta 3 despliega edicion usuario GET

#RUTA 3A
#el html 3 no es un post, la caja que contiene el form es un post, al dar editar en
# este boton colocando los nuevos valores me redireccionará a la ruta 2 con los nuevos valores-

@app.route( '/usuario/editar/<int:id>', methods=["POST"] )
def editarUsuario( id ):
    passwordEncriptado = bcrypt.generate_password_hash( request.form["password"] ) ##ENCRIPTACION 1.9: dentro de los () pongo el request.form password, defino la variable y lo colco en el dicc
    usuarioAEditar = { #vamos a preparar el diccionario
        "id": id,
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
        "password" : passwordEncriptado, ##ENCRIPTACION 1.10
        "dojo_id" : request.form["dojo_id"]
    }
    resultado = Usuario.editarUsuario( usuarioAEditar ) # ahora nos vamos al defModelo "editarUsuario" y añadimos el campo
    print(resultado)
    session["first_name"] = request.form["first_name"] #validacion de la sesion
    session["last_name"] = request.form["last_name"]
    return redirect ( '/dashboard' )
