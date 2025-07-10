import sqlite3
import hashlib
from http.server import BaseHTTPRequestHandler, HTTPServer

# Configuración
PUERTO = 5800
DB_FILE = "usuarios.db"

class AuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            
            html = """
            <html>
                <body style="font-family: Arial; margin: 50px;">
                    <h1>Sistema de Autenticación - DRY7122</h1>
                    <h2>Integrantes: Jean Lopez y Matias Parra</h2>
                    <form action="/login" method="post" style="margin-top: 20px;">
                        <label>Usuario:</label><br>
                        <input type="text" name="usuario" required><br><br>
                        
                        <label>Contraseña:</label><br>
                        <input type="password" name="contrasena" required><br><br>
                        
                        <input type="submit" value="Ingresar" style="padding: 5px 15px;">
                    </form>
                </body>
            </html>
            """
            self.wfile.write(html.encode())
            
    def do_POST(self):
        if self.path == "/login":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length).decode()
            
            datos = dict(pair.split("=") for pair in post_data.split("&"))
            usuario = datos.get("usuario", "")
            contrasena = datos.get("contrasena", "")
            
            if verificar_usuario(usuario, contrasena):
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(b"""
                    <h1 style='color: green;'>Acceso concedido!</h1>
                    <p>Bienvenido al sistema de evaluacion</p>
                """)
            else:
                self.send_response(401)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(b"""
                    <h1 style='color: red;'>Error de autenticacion</h1>
                    <p>Usuario o contrasena incorrectos</p>
                    <a href='/'>Volver a intentar</a>
                """)

def crear_tabla():
    conexion = sqlite3.connect(DB_FILE)
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            contrasena_hash TEXT NOT NULL
        )
    """)
    conexion.commit()
    conexion.close()

def hash_contrasena(contrasena):
    return hashlib.sha256(contrasena.encode()).hexdigest()

def registrar_usuario(usuario, contrasena):
    conexion = sqlite3.connect(DB_FILE)
    cursor = conexion.cursor()
    try:
        cursor.execute(
            "INSERT INTO usuarios (usuario, contrasena_hash) VALUES (?, ?)",
            (usuario, hash_contrasena(contrasena)))
        conexion.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conexion.close()

def verificar_usuario(usuario, contrasena):
    conexion = sqlite3.connect(DB_FILE)
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT contrasena_hash FROM usuarios WHERE usuario = ?",
        (usuario,))
    resultado = cursor.fetchone()
    conexion.close()
    
    return resultado and resultado[0] == hash_contrasena(contrasena)

def main():
    crear_tabla()
    
    # Integrantes actualizados con sus credenciales
    integrantes = [
        ("JeanLopez", "cisco123"),  # Usuario: JeanLopez
        ("MatiasParra", "cisco123")  # Usuario: MatiasParra
    ]
    
    print("=== REGISTRO DE INTEGRANTES ===")
    for usuario, contrasena in integrantes:
        if registrar_usuario(usuario, contrasena):
            print(f" {usuario} registrado correctamente")
        else:
            print(f" {usuario} ya existía en la base de datos")
    
    print("\n=== HASHES DE CONTRASEÑAS ===")
    for usuario, contrasena in integrantes:
        print(f"Usuario: {usuario}")
        print(f"Hash: {hash_contrasena(contrasena)}")
        print("-" * 50)
    
    print(f"\n Servidor iniciado en http://localhost:{PUERTO}")
    print("Presiona Ctrl+C para detenerlo\n")
    
    try:
        servidor = HTTPServer(("localhost", PUERTO), AuthHandler)
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido")

if __name__ == "__main__":
    main()