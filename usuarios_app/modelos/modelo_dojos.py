#necesitamos la conexion a BD, lo mismo del modelo usuarios

from usuarios_app.config.mysqlconnection import connectToMySQL
from usuarios_app.modelos.modelo_usuarios import Usuario


class Dojo:
    def __init__( self, id, name, created_at, updated_at ):
        self.id = id
        self.name = name
        self.created_at = created_at
        self.updated_at = updated_at
        self.usuarios = [] #tercer campo inicialmente como un arreglo vacío
    
    def agregaUsuario( self, usuario ):
        self.usuarios.append( usuario )

    #RUTA 1A Registro para jalar dojos y RUTA 2C Editar. Lo estamos usando en el contorladorU 
    # y lo hemos importado
    @classmethod
    def obtenerListaDojos( cls):
        query = "SELECT * FROM dojos;"
        resultado = connectToMySQL( "users_iniciosesionregist" ).query_db( query )
        listaDojos = []
        for dojo in resultado:
            listaDojos.append( cls( dojo["id"], dojo["name"], dojo["created_at"], dojo["updated_at"])) #Colocar sí o sí todos los atributos que están en el constructor Dojo para que funcione
        return listaDojos


#AQUÍ!!
    @classmethod
    def obtenerListaDojosConUsuarios( cls ): 
        query = "SELECT * FROM dojos d LEFT JOIN usuarios u ON d.id = u.dojo_id;" 
        resultado = connectToMySQL( 'users_iniciosesionregist' ).query_db( query ) 
        listaDojosConUsuarios = []
        
        for renglon in resultado:
            indice = existeDojoEnArreglo( renglon["id"], listaDojosConUsuarios )
            if indice == -1:
                departamentoAAgregar = Dojo(renglon["id"], renglon["name"], renglon["created_at"], renglon["updated_at"]) #Colocar sí o sí todos los atributos que están en el constructor Dojo para que funcione
                departamentoAAgregar.agregaUsuario( Usuario(renglon["u.id"], renglon["first_name"], renglon["last_name"], renglon["email"], renglon["password"], renglon["created_at"], renglon["updated_at"], renglon["dojo_id"]) )
                listaDojosConUsuarios.append( departamentoAAgregar )
            else:
                listaDojosConUsuarios[indice].agregaUsuario( Usuario(renglon["u.id"], renglon["first_name"], renglon["last_name"], renglon["email"], renglon["password"], renglon["created_at"], renglon["updated_at"], renglon["dojo_id"]) )
                
        return listaDojosConUsuarios


def existeDojoEnArreglo( id_doj, listaDepartamentos ):
    for i in range( 0, len(listaDepartamentos) ):
        if listaDepartamentos[i].id == id_doj:
            return i
    return -1  


def agregaUsuario( self, usuario ):
    self.usuarios.append( usuario )


