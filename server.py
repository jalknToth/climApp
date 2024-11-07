# Importa las bibliotecas necesarias
import flask as fk  # Framework web Flask
import weather as wr  # Módulo personalizado para obtener datos del clima
import waitress as wss  # Servidor WSGI de producción para Flask
import mysql.connector as sql  # Conector para MySQL
import datetime as dt  # Para trabajar con fechas y horas


# Crea una instancia de la aplicación Flask
app = fk.Flask(__name__)

# Función para establecer la conexión a la base de datos MySQL
def getDBconnection():
    conn = sql.connect(
        host='localhost',  # Host de la base de datos
        user='root',  # Usuario de la base de datos
        password='',  # Contraseña del usuario
        database='climapp'  # Nombre de la base de datos
    )
    return conn

# Función para guardar los datos del clima en la base de datos
def guardarDatos(ciudad, temperatura, descripcion):
    conn = getDBconnection()  # Obtiene la conexión a la base de datos
    cur = conn.cursor()  # Crea un cursor para ejecutar consultas
    now = dt.datetime.now()  # Obtiene la fecha y hora actual

    try:
        # Inserta los datos en la tabla 'clima'
        cur.execute('INSERT INTO clima (ciudad, temperatura, descripcion, fecHora) VALUES (%s, %s, %s, %s)',(ciudad, temperatura, descripcion, now))
        conn.commit()  # Confirma los cambios
    except sql.Error as err:  # Maneja errores de SQL
        print(f"Error al guardar los datos: {err}")
        conn.rollback()  # Revierte los cambios en caso de error
    finally:
        cur.close()  # Cierra el cursor
        conn.close()  # Cierra la conexión


# Define la ruta principal de la aplicación
@app.route('/')
@app.route('/index') # también responde a /index
def index():
    return fk.render_template('index.html')  # Renderiza la plantilla 'index.html'


# Define la ruta para obtener el clima
@app.route('/weather')
def get_weather():
    city = fk.request.args.get('city')  # Obtiene el parámetro 'city' de la URL

    # Si la ciudad no se proporciona o está vacía, se establece por defecto a "Medellin"
    if city is None or not city.strip():
        city = "Medellin"

    # Llama a la función 'revisarClima' del módulo 'weather' para obtener los datos del clima
    weather_data = wr.revisarClima(city)

    # Manejo de errores:
    if weather_data is None:
        return fk.render_template('error.html', error_message="Error al obtener los datos del clima."), 500  # Error 500: Internal Server Error

    if weather_data['cod'] != 200: # Si la API del clima devuelve un código distinto a 200 (OK)
        return fk.render_template('error.html', ciudad=city), 404  # Error 404: Not Found

    # Guarda los datos del clima en la base de datos
    guardarDatos(weather_data["name"], weather_data['main']['temp'], weather_data["weather"][0]["description"])

    # Renderiza la plantilla 'weather.html' con los datos del clima
    return fk.render_template(
        "weather.html",
        title=weather_data["name"],
        status=weather_data["weather"][0]["description"].capitalize(),
        temp=f"{weather_data['main']['temp']:.1f}", # Formatea la temperatura a un decimal
        feels_like=f"{weather_data['main']['feels_like']:.1f}" # Formatea la sensación térmica a un decimal
    )

# Función para crear la tabla 'clima' en la base de datos si no existe
def creaTable():
    conn = getDBconnection()
    cur = conn.cursor()

    try:
        # Crea la tabla 'clima'
        cur.execute('''CREATE TABLE IF NOT EXISTS clima (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        ciudad VARCHAR(255) NOT NULL,
                        temperatura FLOAT,
                        descripcion VARCHAR(255),
                        fecHora DATETIME
                    )''')
        conn.commit()
    except sql.Error as err:
        print(f"Error al crear la tabla: {err}")
    finally:
        cur.close()
        conn.close()

# Punto de entrada principal del script
if __name__ == "__main__":
    creaTable()  # Crea la tabla al iniciar la aplicación
    wss.serve(app, host="0.0.0.0", port=8000)  # Inicia el servidor Waitress en el puerto 8000 (para producción)
