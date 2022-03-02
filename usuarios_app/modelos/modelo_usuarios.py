from usuarios_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') #EmailExprReg

class Usuario:
    def __init__( self, id, first_name, last_name, email, password, created_at, updated_at, dojo_id ): #colocamos todo los atributos de la tabla
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.created_at = created_at
        self.updated_at = updated_at
        self.dojo_id = dojo_id

        #RUTA 1A. Registrar acá insertamos los nuevos usuarios
        # "y" Se hace cambios para permitir que el usuario se registre con su dojo
    @classmethod
    def agregaUsuario( cls, nuevoUsuario ): #diccionario creado
        query = "INSERT INTO usuarios(first_name, last_name, email, password, dojo_id) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(dojo_id)s);" #colocamos insert de lo que solo insertaremos en el form Registro
        resultado= connectToMySQL( "users_iniciosesionregist" ).query_db( query, nuevoUsuario )
        return resultado #se lo vamos a devolver al controlador

#Ruta 1A POST Registro- Validar los datos insertados antes de hacer el insert oficial
    #validamos que el email no sea registrado dos veces
    @staticmethod
    def validarRegistro(nuevoUsuario):
        esValido = True
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        resultado = connectToMySQL( "users_iniciosesionregist" ).query_db(query,nuevoUsuario)
        if len(resultado) >= 1: #validamos que el email no sea registrado dos veces, llamamos al query 
            #con un select para comprobar los email
            flash("Email already taken.","registro")
            esValido= False
        if not EMAIL_REGEX.match(nuevoUsuario['email']): #validamos que la expreg del email esté bien escrita
            flash("Invalid Email!!!","registro")
            esValido= False
        if len(nuevoUsuario['first_name']) < 3: #nombre f
            flash("First name must be at least 3 characters","registro")
            esValido= False
        if len(nuevoUsuario['last_name']) < 3: #apellido f
            flash("Last name must be at least 3 characters","registro")
            esValido= False
        if len(nuevoUsuario['password']) < 8: #password f
            flash("Password must be at least 8 characters","registro")
            esValido= False
        if nuevoUsuario['password'] != nuevoUsuario['confirmPassword']: #acá comprobamos que la casilla password y confirm deben ser las mismas
            #so la condicion dice que si son diferentes != salga mensaje de flash que es un F y retorne un F 
            flash("Passwords don't match","registro")
        return esValido





























        #RUTA 1B. Login acá vamos a seleccionar solo los usuarios que se han registrado
        # Instancias de Objeto Usuario. Eso lo hacemos porque debemos ser consistentes, hemos modificado el constructor, 
        # por ende, donde hice instancias de objeto Usuario, añadir el xxxxx[0]["id_departamento"]-
    @classmethod #controlador ruta 1B para el login, estamos creando un query para el login exitoso
    def verificaUsuario( cls, usuario ): #queremos un diccionario para el login que tendrá el email y password, en los () colocamos cls y usuario porque ya no es nuevoUsuario ahora ya es un usuario, 
        query = "SELECT * FROM usuarios WHERE email = %(email)s;" ##ENCRIPTACION 1.8: eliminamos el password del select porque acá está comparando el pasword encriptado del controlador contra el password noraml de la BD
        resultado = connectToMySQL( "users_iniciosesionregist" ).query_db( query, usuario )
        if len( resultado ) > 0:
            usuarioResultado = Usuario( resultado[0] ["id"], resultado[0] ["first_name"], resultado[0] ["last_name"], resultado[0] ["email"], resultado[0] ["password"], resultado[0] ["created_at"], resultado[0] ["updated_at"], resultado[0] ["dojo_id"] ) #añadimos toda la tabla usuarios incluyendo id PK y el FK
            return usuarioResultado
        else:
            return None


        #RUTA 2 ver el portal tabla con usuarios /
        
        #RUTA 2A
        # Instancias de Objeto Usuario. Eso lo hacemos porque debemos ser consistentes, hemos modificado el constructor, 
        # por ende, donde hice instancias de objeto Usuario, añadir el xxxxx[0]["id_departamento"]-
    @classmethod
    def obtenerListaUsuarios( self ):
        query = "SELECT * FROM usuarios;"
        resultado = connectToMySQL( "users_iniciosesionregist" ).query_db( query )
        listaUsuarios = []
        for usuario in resultado:
            listaUsuarios.append( Usuario( usuario["id"], usuario["first_name"], usuario["last_name"], usuario["email"], usuario["password"], usuario["created_at"], usuario["updated_at"], usuario["dojo_id"])) #añadimos toda la tabla usuarios incluyendo id PK y el FK
        return listaUsuarios

        #RUTA 2B Eliminar
    @classmethod
    def eliminarUsuario( self, usuario ):
        query = "DELETE FROM usuarios WHERE id = %(id)s;"
        resultado = connectToMySQL( "users_iniciosesionregist" ).query_db( query, usuario )
        return resultado

        #Ruta 2C boton Editar (GET), no se añade informacion por eso es GET, click y renderiza a Ruta 3 template, antes de renderizarlo vamos a jalar los datos del id en el controlador-
    @classmethod
    def obtenerDatosUsuario( self, usuario ):
        query = "SELECT * FROM usuarios WHERE id = %(id)s;"
        resultado = connectToMySQL( "users_iniciosesionregist" ).query_db( query, usuario )
        return resultado

        #RUTA 3A #el html 3 no es un post, la caja que contiene el form es un post
        # "y" Vamos a permitir al usuario cambiar de departamento, por eso añadimos el campo departamento
    @classmethod
    def editarUsuario( self, usuarioAEditar ):
        query = "UPDATE usuarios SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, password = %(password)s, dojo_id = %(dojo_id)s WHERE id = %(id)s;" #el Where es el id PK de la tabla principal
        resultado = connectToMySQL( "users_iniciosesionregist" ).query_db( query, usuarioAEditar )
        return resultado
