import tkinter as tk
import sqlite3

# Funcion para crear o conectar a la base de datos y crear la tabla de usuarios
def crear_base_datos():
    conn = sqlite3.connect("asesorias.db")
    cursor = conn.cursor()

    # Crear tabla de usuarios si no existe
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                        id INTEGER PRIMARY KEY,
                        nombre TEXT NOT NULL,
                        apellido TEXT NOT NULL,
                        correo TEXT NOT NULL UNIQUE,
                        contrasena TEXT NOT NULL)''')

    # Crear tabla de historial de asesorias si no existe
    cursor.execute('''CREATE TABLE IF NOT EXISTS historial_asesorias (
                        id INTEGER PRIMARY KEY,
                        usuario_id INTEGER,
                        tema TEXT NOT NULL,
                        fecha TEXT NOT NULL,
                        FOREIGN KEY (usuario_id) REFERENCES usuarios (id))''')

    conn.commit()
    conn.close()

def agregar_asesoria(usuario_id, tema, fecha):
    conn = sqlite3.connect("asesorias.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO historial_asesorias (usuario_id, tema, fecha) VALUES (?, ?, ?)",
                   (usuario_id, tema, fecha))

    conn.commit()
    conn.close()


# Funcion para registrar un nuevo usuario
def registrar_usuario(nombre, apellido, correo, password):
    if not (nombre and apellido and correo and password):
        mostrar_mensaje("Todos los campos son obligatorios", "error")
        return
    
    conexion = sqlite3.connect('usuarios.db')
    cursor = conexion.cursor()

    # Insertar los datos del usuario en la tabla
    try:
        cursor.execute("INSERT INTO usuarios (nombre, apellido, correo, password) VALUES (?, ?, ?, ?)",
                       (nombre, apellido, correo, password))
        conexion.commit()
        mostrar_mensaje("¡Registro exitoso!", "exito")
    except sqlite3.IntegrityError:
        mostrar_mensaje("El correo ya está registrado.", "error")
    
    conexion.close()

# Funcion para validar los datos de inicio de sesion
def iniciar_sesion(correo, password):
    if not (correo and password):
        mostrar_mensaje("Correo y contraseña son obligatorios", "error")
        return

    conexion = sqlite3.connect('usuarios.db')
    cursor = conexion.cursor()

    # Buscar al usuario por correo y contraseña
    cursor.execute("SELECT * FROM usuarios WHERE correo = ? AND password = ?", (correo, password))
    usuario = cursor.fetchone()
    
    if usuario:
        mostrar_mensaje(f"¡Bienvenido, {usuario[1]}!", "exito")
        ventana_principal.user_id = usuario[0]  # Guardar el ID del usuario en la ventana
        mostrar_pantalla_inicio()
    else:
        mostrar_mensaje("Error: Correo o contraseña incorrectos", "error")

    conexion.close()

# Funcion para mostrar un mensaje en la interfaz
def mostrar_mensaje(mensaje, tipo):
    label_mensaje = tk.Label(ventana_principal, text=mensaje, font=("Arial", 12), 
                              fg="green" if tipo == "exito" else "red", bg="#2E8B57")
    label_mensaje.pack(pady=10)

# Funciones para mostrar las diferentes pantallas

def mostrar_formulario_registro():
    # Limpiar la ventana antes de mostrar el formulario de registro
    for widget in ventana_principal.winfo_children():
        widget.destroy()

    label_titulo = tk.Label(ventana_principal, text="Registro", font=("Arial", 16, "bold"), 
                            bg="#2E8B57", fg="white")
    label_titulo.pack(pady=20)

    label_nombre = tk.Label(ventana_principal, text="Nombre:", font=("Arial", 12), bg="#2E8B57", fg="white")
    entry_nombre = tk.Entry(ventana_principal, font=("Arial", 12), width=30)
    label_nombre.pack(pady=5)
    entry_nombre.pack(pady=5)

    label_apellido = tk.Label(ventana_principal, text="Apellido:", font=("Arial", 12), bg="#2E8B57", fg="white")
    entry_apellido = tk.Entry(ventana_principal, font=("Arial", 12), width=30)
    label_apellido.pack(pady=5)
    entry_apellido.pack(pady=5)

    label_correo = tk.Label(ventana_principal, text="Correo:", font=("Arial", 12), bg="#2E8B57", fg="white")
    entry_correo = tk.Entry(ventana_principal, font=("Arial", 12), width=30)
    label_correo.pack(pady=5)
    entry_correo.pack(pady=5)

    label_password = tk.Label(ventana_principal, text="Contraseña:", font=("Arial", 12), bg="#2E8B57", fg="white")
    entry_password = tk.Entry(ventana_principal, show="*", font=("Arial", 12), width=30)
    label_password.pack(pady=5)
    entry_password.pack(pady=5)

    button_aceptar = tk.Button(ventana_principal, text="Aceptar", font=("Arial", 12), 
                                command=lambda: registrar_usuario(entry_nombre.get(), entry_apellido.get(), 
                                                                  entry_correo.get(), entry_password.get()), 
                                bg="#4CAF50", fg="white")
    button_aceptar.pack(pady=10)

    button_volver = tk.Button(ventana_principal, text="Volver", font=("Arial", 12), command=mostrar_ventana_principal, 
                              bg="#f44336", fg="white")
    button_volver.pack(pady=10)

def mostrar_formulario_ingreso():
    # Limpiar la ventana antes de mostrar el formulario de inicio de sesion
    for widget in ventana_principal.winfo_children():
        widget.destroy()

    label_titulo = tk.Label(ventana_principal, text="Iniciar Sesión", font=("Arial", 16, "bold"), 
                            bg="#2E8B57", fg="white")
    label_titulo.pack(pady=20)

    label_correo = tk.Label(ventana_principal, text="Correo:", font=("Arial", 12), bg="#2E8B57", fg="white")
    entry_correo = tk.Entry(ventana_principal, font=("Arial", 12), width=30)
    label_correo.pack(pady=5)
    entry_correo.pack(pady=5)

    label_password = tk.Label(ventana_principal, text="Contraseña:", font=("Arial", 12), bg="#2E8B57", fg="white")
    entry_password = tk.Entry(ventana_principal, show="*", font=("Arial", 12), width=30)
    label_password.pack(pady=5)
    entry_password.pack(pady=5)

    button_ingresar = tk.Button(ventana_principal, text="Iniciar Sesión", font=("Arial", 12), 
                                 command=lambda: iniciar_sesion(entry_correo.get(), entry_password.get()), 
                                 bg="#4CAF50", fg="white")
    button_ingresar.pack(pady=10)

    button_volver = tk.Button(ventana_principal, text="Volver", font=("Arial", 12), command=mostrar_ventana_principal, 
                              bg="#f44336", fg="white")
    button_volver.pack(pady=10)

def mostrar_pantalla_inicio():
    # Limpiar la ventana principal antes de mostrar el inicio
    for widget in ventana_principal.winfo_children():
        widget.destroy()

    label_bienvenida = tk.Label(ventana_principal, text="Bienvenido al Sistema de Asesorías", 
                                 font=("Arial", 16, "bold"), bg="#2E8B57", fg="white")
    label_bienvenida.pack(pady=20)

    # Botón para ver asesorías
    button_asesorias = tk.Button(ventana_principal, text="Ver Asesorías", font=("Arial", 12), 
                                  command=mostrar_pantalla_asesorias, bg="#4CAF50", fg="white")
    button_asesorias.pack(pady=10)

    # Botón para ver historial
    button_historial = tk.Button(ventana_principal, text="Ver Historial", font=("Arial", 12), 
                                  command=mostrar_pantalla_historial, bg="#4CAF50", fg="white")
    button_historial.pack(pady=10)

    # Botón para ir a configuraciones
    button_configuracion = tk.Button(ventana_principal, text="Configuraciones", font=("Arial", 12), 
                                      command=mostrar_pantalla_configuraciones, bg="#4CAF50", fg="white")
    button_configuracion.pack(pady=10)

    # Botón para cerrar sesión
    button_salir = tk.Button(ventana_principal, text="Cerrar sesión", font=("Arial", 12), 
                             command=mostrar_ventana_principal, bg="#f44336", fg="white")
    button_salir.pack(pady=20)

def mostrar_pantalla_asesorias():
    # Limpiar la ventana antes de mostrar asesorias
    for widget in ventana_principal.winfo_children():
        widget.destroy()

    label_titulo = tk.Label(ventana_principal, text="Asesorías Disponibles", font=("Arial", 16, "bold"), 
                            bg="#2E8B57", fg="white")
    label_titulo.pack(pady=20)

    # Aquí puedes añadir los temas de asesoria
    temas = ["Matemáticas", "Programación", "Ciencias", "Historia"]
    for tema in temas:
        label_tema = tk.Label(ventana_principal, text=tema, font=("Arial", 12), bg="#2E8B57", fg="white")
        label_tema.pack(pady=5)

    button_volver = tk.Button(ventana_principal, text="Volver", font=("Arial", 12), command=mostrar_pantalla_inicio, 
                              bg="#f44336", fg="white")
    button_volver.pack(pady=10)

def mostrar_pantalla_historial():
    # Limpiar la ventana antes de mostrar el historial
    for widget in ventana_principal.winfo_children():
        widget.destroy()

    label_titulo = tk.Label(ventana_principal, text="Historial de Asesorías", font=("Arial", 16, "bold"), 
                            bg="#2E8B57", fg="white")
    label_titulo.pack(pady=20)

    # Aqui puedes añadir el historial de asesorias
    # Ejemplo: Consultar historial desde la base de datos
    button_volver = tk.Button(ventana_principal, text="Volver", font=("Arial", 12), command=mostrar_pantalla_inicio, 
                              bg="#f44336", fg="white")
    button_volver.pack(pady=10)

def mostrar_pantalla_configuraciones():
    # Limpiar la ventana antes de mostrar configuraciones
    for widget in ventana_principal.winfo_children():
        widget.destroy()

    label_titulo = tk.Label(ventana_principal, text="Configuraciones", font=("Arial", 16, "bold"), 
                            bg="#2E8B57", fg="white")
    label_titulo.pack(pady=20)

    # Aqui puedes añadir opciones de configuracion
    button_volver = tk.Button(ventana_principal, text="Volver", font=("Arial", 12), command=mostrar_pantalla_inicio, 
                              bg="#f44336", fg="white")
    button_volver.pack(pady=10)

# Funcion para mostrar la ventana principal
def mostrar_ventana_principal():
    # Limpiar la ventana antes de mostrar la pantalla principal
    for widget in ventana_principal.winfo_children():
        widget.destroy()

    label_titulo = tk.Label(ventana_principal, text="Sistema de Asesorías", font=("Arial", 16, "bold"), 
                            bg="#2E8B57", fg="white")
    label_titulo.pack(pady=20)

    button_registro = tk.Button(ventana_principal, text="Registrarse", font=("Arial", 12), 
                                 command=mostrar_formulario_registro, bg="#4CAF50", fg="white")
    button_registro.pack(pady=10)

    button_ingreso = tk.Button(ventana_principal, text="Iniciar Sesión", font=("Arial", 12), 
                                command=mostrar_formulario_ingreso, bg="#4CAF50", fg="white")
    button_ingreso.pack(pady=10)

# Crear la ventana principal
ventana_principal = tk.Tk()
ventana_principal.title("Sistema de Asesorías")
ventana_principal.geometry("400x500")
ventana_principal.configure(bg="#2E8B57")

crear_base_datos()  # Crear base de datos al iniciar
mostrar_ventana_principal()  # Mostrar pantalla inicial

ventana_principal.mainloop()
