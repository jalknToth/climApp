import mysql.connector as sql

# Configuración de la conexión
config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'arpa'  
}

try:
    # Conexión a la base de datos
    cnx = sql.connect(**config)
    cursor = cnx.cursor()

    # Consulta SQL para crear la tabla "usuarios"
    sql = """
    CREATE TABLE IF NOT EXISTS usuarios (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(255) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        contrasena VARCHAR(255) NOT NULL 
    )
    """ 
    cursor.execute(sql)

    print("Tabla 'usuarios' creada con éxito (o ya existe)")

    cnx.commit()  # Guardar los cambios en la base de datos
    
# Corrección: Usar mysql.connector.Error
except sql.connector.Error as err:  
    print(f"Error: {err}")

finally:
    # Cerrar la conexión
    if cnx.is_connected():
        cursor.close()
        cnx.close()