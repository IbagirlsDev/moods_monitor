from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
import os
from dotenv import load_dotenv
from openpyxl import Workbook
from io import BytesIO
import traceback


# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')  # Clave secreta para la sesión

# Función para conectar a la base de datos usando un gestor de contexto
class DatabaseConnection:
    def __enter__(self):
        try:
            print("Error al conectar a la base de datos:")
            traceback.print_exc()
            
            self.conn=psycopg2.connect( 
                dbname=os.getenv('DB_NAME'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                host=os.getenv('DB_HOST'),
                port=os.getenv('DB_PORT')
            )
            self.cur = self.conn.cursor()
            return self.cur
        except Exception as e:
            print(f"Error al conectar a la base de datos: {e}")
            raise

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.cur.close()
        self.conn.close()

@app.route('/')
def index():
    return render_template('inicio.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        with DatabaseConnection() as cur:
            cur.execute('SELECT * FROM usuarios WHERE username = %s', (username,))
            user = cur.fetchone()

        if user and check_password_hash(user[4], password):
            session['user_id'] = user[0]
            session['tipo_usuario_id'] = user[5]
            
            if user[5] == 1:  # Administrador
                return redirect(url_for('admin_dashboard'))
            else:  # Usuario
                return redirect(url_for('usuario_dashboard'))
        else:
            flash('Credenciales inválidas.')
        
    # Manejo de la redirección desde el index.html
    tipo_usuario = request.args.get('tipo')
    return render_template('login.html', tipo_usuario=tipo_usuario)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        password = request.form['password']
        tipo_usuario_id = 2
        email = request.form['email']            
        
            # Validación de campos
        if not all([first_name, last_name, username, email, password]):
            flash('Todos los campos son requeridos.')
            return redirect(url_for('register'))
        
        try:            
            
            with DatabaseConnection() as cur:
                cur.execute('SELECT * FROM usuarios WHERE username = %s', (username,))
                user_exists = cur.fetchone()

                if user_exists:
                    flash('El nombre de usuario ya están en uso.')
                    return redirect(url_for('register'))
                
                cur.execute('SELECT * FROM usuarios WHERE email = %s', (email,))
                email_exists = cur.fetchone()

                if email_exists:
                    flash('El correo electrónico ya está en uso.')
                    return redirect(url_for('register'))

                cur.execute('INSERT INTO usuarios (first_name, last_name, username, password, tipo_usuario_id, email) VALUES (%s, %s, %s, %s, %s, %s)', 
                            (first_name, last_name, username, generate_password_hash(password), tipo_usuario_id, email)) 

            flash('Registro exitoso. Ahora puedes iniciar sesión.')
            return redirect(url_for('login'))
        
        except psycopg2.Error as e:
            flash(f'Error en la base de datos: {e}')
            return redirect(url_for('register'))
        except Exception as e:
            flash(f'Ocurrió un error: {e}')
            return redirect(url_for('register'))

    return render_template('registro.html')

@app.route('/admin')
def admin_dashboard():
    if session.get('tipo_usuario_id') == 1:
        return render_template('admin.html')
    return redirect(url_for('login'))

@app.route('/asistente_virtual')
def asistente_virtual():
    if session.get('tipo_usuario_id') != 2:
        return redirect(url_for('login'))
    
    emocion_id = request.args.get('emocion_id', None)
    return render_template('asistente_virtual.html', emocion_id=emocion_id)

@app.route('/usuario', methods=['GET', 'POST'])
def usuario_dashboard():
    if session.get('tipo_usuario_id') != 2:
        return redirect(url_for('login'))

    if request.method == 'POST':
        email = request.form['email']
        emocion_id = request.form['emoji']
        opcion = request.form['emotion-options']
        razon = request.form['reason']
        
        print(emocion_id)  # Verifica que el emocion_id se esté obteniendo correctamente

        user = obtener_usuario_por_email(email)
        if not user:
            flash('El usuario no está registrado.')
            return redirect(url_for('usuario_dashboard'))

        try:
            registrar_estado_animo(user[0], emocion_id, opcion, razon)
            if emocion_id != '0': 
                return redirect(url_for('asistente_virtual', emocion_id=emocion_id))  # Redirige a asistente virtual
            
        except psycopg2.Error as e:
            flash(f'Error en la base de datos: {e}')
        except Exception as e:
            flash('Ocurrió un error.')

        return redirect(url_for('usuario_dashboard'))

    return render_template('usuario.html')


def obtener_usuario_por_email(email):
    with DatabaseConnection() as cur:
        cur.execute('SELECT * FROM usuarios WHERE email = %s', (email,))
        user = cur.fetchone()
    return user

def registrar_estado_animo(user_id, emocion_id, opcion, razon):
    with DatabaseConnection() as cur:
        cur.execute(
            'INSERT INTO estados_animo (user_id, emocion_id, opcion, razon) VALUES (%s, %s, %s, %s)', 
            (user_id, emocion_id, opcion, razon)
        )

# Cerrar sesión
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    session.pop('admin', None)
    session.clear()  # Esto elimina todos los datos de la sesión
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('login'))  # Redirige al login

# Ruta para probar la conexión a la base de datos
@app.route('/test_db')
def test_db():
    try:
        with DatabaseConnection() as cur:
            cur.execute('SELECT 1')
            result = cur.fetchone()

            if result:
                return 'Conexión exitosa a la base de datos'
            return 'Error al ejecutar la consulta de prueba'
    except Exception as e:
        return f'Error al conectar a la base de datos: {e}'

# Ruta para descargar el informe de los estados de ánimo
@app.route('/download_data')
def download_data():
    if session.get('tipo_usuario_id') == 1:
        try:
            with DatabaseConnection() as cur:
                cur.execute("""
                    SELECT DATE(ea.created_at) AS fecha_registro, u.first_name, u.last_name, u.email, e.nombre AS emocion, ea.opcion, ea.razon 
                    FROM estados_animo ea
                    JOIN usuarios u ON ea.user_id = u.id
                    JOIN emociones e ON ea.emocion_id = e.id
                    ORDER BY ea.created_at DESC
                """)
                rows = cur.fetchall()

            wb = Workbook()
            ws = wb.active
            ws.title = 'Estados de Ánimo'
            # Agregar los encabezados
            ws.append(['Fecha', 'Nombre', 'Apellido', 'Email', 'Emoción', 'opcion', 'Razón'])

            # Agregar los datos de los usuarios
            for row in rows:
                ws.append(row)
            # Guardar el archivo en memoria
            output = BytesIO()
            wb.save(output)
            output.seek(0)
            # Enviar el archivo al navegador
            return send_file(output, as_attachment=True, download_name="informe_estados_animo.xlsx", mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        except psycopg2.Error as e:
            flash(f'Error al generar el informe: {e}')
            return redirect(url_for('admin_dashboard'))
        except Exception as e:
            flash('Ocurrió un error.')
            return redirect(url_for('admin_dashboard'))
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
