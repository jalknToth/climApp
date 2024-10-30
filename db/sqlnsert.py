import mysql.connector as sql
import pandas as pd

# Configuración de la conexión
config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'climapp'  
}

try:
    # Conexión a la base de datos
    cnx = sql.connect(**config)
    cursor = cnx.cursor()

    # Crear la tabla 'datosClima' si no existe
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS datosClima (
            id INT AUTO_INCREMENT PRIMARY KEY,
            ciudad VARCHAR(255) NOT NULL,
            apellido VARCHAR(255) NOT NULL,
            salario DECIMAL(10,2) 
        )
    """)

    # Insertar datos en la tabla 'datosClima'
    sql = "INSERT INTO datosClima (empleadoID, nombre, apellido, salario) VALUES (%s, %s, %s, %s)"
    for index, row in df.iterrows():
        valores = (row['empleadoID'],row['nombre'], row['apellido'], row['salario'])
        cursor.execute(sql, valores)

    cnx.commit()
    print("Datos insertados con éxito desde el archivo Excel.")

except sql.Error as err:  
    print(f"Error: {err}")

finally:
    if cnx.is_connected():
        cursor.close()
        cnx.close()