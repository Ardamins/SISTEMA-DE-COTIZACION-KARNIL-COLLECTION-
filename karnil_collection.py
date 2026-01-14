import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
from datetime import datetime
import csv
import os
import hashlib
import json
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
import webbrowser

class SistemaLogin:
    def __init__(self, root):
        self.root = root
        self.root.title("KARNIL COLLECTION - Login")
        self.root.geometry("400x500")
        
        self.centrar_ventana(400, 500)
        
        self.color_verde_oscuro = "#006400"
        self.color_verde = "#228B22"
        self.color_verde_claro = "#90EE90"
        self.color_fondo = "#F0FFF0"
        
        self.root.configure(bg=self.color_fondo)
        
        self.inicializar_base_datos()
        self.mostrar_login()
    
    def centrar_ventana(self, ancho, alto):
        """Centrar ventana en la pantalla"""
        pantalla_ancho = self.root.winfo_screenwidth()
        pantalla_alto = self.root.winfo_screenheight()
        x = (pantalla_ancho // 2) - (ancho // 2)
        y = (pantalla_alto // 2) - (alto // 2)
        self.root.geometry(f'{ancho}x{alto}+{x}+{y}')
    
    def inicializar_base_datos(self):
        """Inicializar base de datos con usuarios y productos"""
        conn = sqlite3.connect("karnil.db")
        c = conn.cursor()
        
        # Tabla de usuarios
        c.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT,
                    nombre TEXT,
                    rol TEXT DEFAULT 'vendedor')''')
        
        # Tabla de productos
        c.execute('''CREATE TABLE IF NOT EXISTS productos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    codigo TEXT UNIQUE,
                    nombre TEXT,
                    precio_base REAL,
                    precio_mayor REAL,
                    tallas_cantidades TEXT,
                    precios_tallas TEXT,
                    colores_tallas TEXT,
                    colores_disponibles TEXT,
                    tipo_material TEXT,
                    fecha_creacion TEXT DEFAULT CURRENT_TIMESTAMP,
                    fecha_modificacion TEXT DEFAULT CURRENT_TIMESTAMP)''')
        
        # Tabla de cotizaciones
        c.execute('''CREATE TABLE IF NOT EXISTS cotizaciones (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    numero TEXT UNIQUE,
                    fecha TEXT,
                    cliente_nombre TEXT,
                    cliente_documento TEXT,
                    cliente_tipo TEXT,
                    telefono TEXT,
                    email TEXT,
                    direccion TEXT,
                    subtotal REAL,
                    igv REAL,
                    total REAL,
                    con_igv INTEGER DEFAULT 1,
                    estado TEXT DEFAULT 'PENDIENTE',
                    usuario_id INTEGER,
                    fecha_creacion TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (usuario_id) REFERENCES usuarios(id))''')
        
        # Tabla de detalles de cotización
        c.execute('''CREATE TABLE IF NOT EXISTS cotizacion_detalles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cotizacion_id INTEGER,
                    producto_id INTEGER,
                    producto_nombre TEXT,
                    talla TEXT,
                    cantidad INTEGER,
                    precio_unitario REAL,
                    color TEXT,
                    material TEXT,
                    FOREIGN KEY (cotizacion_id) REFERENCES cotizaciones(id) ON DELETE CASCADE)''')
        
        # Insertar usuarios si no existen
        usuarios = [
            ('ashu', self.encriptar('ashu123'), 'Ashu Salazar', 'admin'),
            ('balu', self.encriptar('balu123'), 'Balu Salazar', 'vendedor'),
            ('sonia', self.encriptar('sonia123'), 'Sonia Rimache', 'vendedor')
        ]
        
        for user in usuarios:
            try:
                c.execute("INSERT OR IGNORE INTO usuarios (username, password, nombre, rol) VALUES (?, ?, ?, ?)", user)
            except:
                pass
        
        # Insertar productos de ejemplo si no existen
        productos = [
            ('CAM-001', 'Camisa Formal Hombre', 45.00, 40.00, 
             '{"S": 10, "M": 15, "L": 20, "XL": 8}', 
             '{"S": 45.00, "M": 45.00, "L": 45.00, "XL": 45.00}',
             '{"S": ["Blanco", "Azul"], "M": ["Blanco", "Azul", "Negro"], "L": ["Azul", "Negro"], "XL": ["Blanco"]}',
             '["Blanco", "Azul", "Negro"]',
             'Algodón 100%'),
            ('VES-001', 'Vestido Elegante Mujer', 85.00, 75.00, 
             '{"S": 5, "M": 8, "L": 6}', 
             '{"S": 85.00, "M": 85.00, "L": 85.00}',
             '{"S": ["Rojo", "Negro"], "M": ["Rojo", "Negro", "Blanco"], "L": ["Negro", "Blanco"]}',
             '["Rojo", "Negro", "Blanco"]',
             'Seda Natural')
        ]
        
        for prod in productos:
            try:
                c.execute("""INSERT OR IGNORE INTO productos (codigo, nombre, precio_base, precio_mayor, 
                          tallas_cantidades, precios_tallas, colores_tallas, colores_disponibles, tipo_material) 
                          VALUES (?,?,?,?,?,?,?,?,?)""", prod)
            except:
                pass
        
        conn.commit()
        conn.close()
    
    def encriptar(self, texto):
        """Encriptar texto simple"""
        return hashlib.sha256(texto.encode()).hexdigest()
    
    def mostrar_login(self):
        """Mostrar pantalla de login"""
        self.limpiar_ventana()
        
        main_frame = tk.Frame(self.root, bg=self.color_fondo)
        main_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        tk.Label(main_frame, text="KARNIL COLLECTION", 
                font=("Arial", 24, "bold"),
                bg=self.color_fondo, fg=self.color_verde_oscuro).pack(pady=20)
        
        tk.Label(main_frame, text="Sistema de Cotización Textil",
                font=("Arial", 12),
                bg=self.color_fondo, fg=self.color_verde).pack(pady=5)
        
        login_frame = tk.Frame(main_frame, bg=self.color_fondo)
        login_frame.pack(pady=30)
        
        tk.Label(login_frame, text="Usuario:", 
                font=("Arial", 12), bg=self.color_fondo).grid(row=0, column=0, pady=10, padx=5, sticky='e')
        self.entry_usuario = tk.Entry(login_frame, font=("Arial", 12), width=20)
        self.entry_usuario.grid(row=0, column=1, pady=10, padx=5)
        
        tk.Label(login_frame, text="Contraseña:", 
                font=("Arial", 12), bg=self.color_fondo).grid(row=1, column=0, pady=10, padx=5, sticky='e')
        self.entry_password = tk.Entry(login_frame, font=("Arial", 12), show="*", width=20)
        self.entry_password.grid(row=1, column=1, pady=10, padx=5)
        
        tk.Button(main_frame, text="Iniciar Sesión", 
                 font=("Arial", 12, "bold"),
                 bg=self.color_verde, fg="white",
                 command=self.verificar_login,
                 width=15, height=2).pack(pady=20)
        
        info_frame = tk.Frame(main_frame, bg=self.color_fondo)
        info_frame.pack(pady=20)
        
        info_text = """Usuarios disponibles:
        • ashu / ashu123 (Administrador)
        • balu / balu123 (Vendedor)
        • sonia / sonia123 (Vendedor)"""
        
        tk.Label(info_frame, text=info_text, 
                bg=self.color_fondo, font=("Arial", 9),
                justify=tk.LEFT).pack()
    
    def limpiar_ventana(self):
        """Limpiar todos los widgets"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def verificar_login(self):
        """Verificar credenciales del usuario"""
        usuario = self.entry_usuario.get().strip()
        password = self.entry_password.get().strip()
        
        if not usuario or not password:
            messagebox.showerror("Error", "Por favor ingrese usuario y contraseña")
            return
        
        conn = sqlite3.connect("karnil.db")
        c = conn.cursor()
        c.execute("SELECT id, nombre, rol FROM usuarios WHERE username = ? AND password = ?", 
                 (usuario, self.encriptar(password)))
        resultado = c.fetchone()
        conn.close()
        
        if resultado:
            self.usuario_actual = {
                'id': resultado[0],
                'nombre': resultado[1],
                'rol': resultado[2]
            }
            self.abrir_cotizador()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
    
    def abrir_cotizador(self):
        """Abrir el sistema de cotización"""
        self.limpiar_ventana()
        CotizadorKarnil(self.root, self.usuario_actual)

class CotizadorKarnil:
    def __init__(self, root, usuario):
        self.root = root
        self.usuario = usuario
        
        self.root.title(f"KARNIL COLLECTION - Bienvenido: {usuario['nombre']} | {usuario['rol'].upper()}")
        self.root.geometry("1400x800")
        
        self.centrar_ventana(1400, 800)
        
        self.color_verde_oscuro = "#006400"
        self.color_verde = "#228B22"
        self.color_verde_claro = "#90EE90"
        self.color_gris_claro = "#F0FFF0"
        self.color_rojo = "#FF4444"
        
        self.root.configure(bg=self.color_gris_claro)
        
        self.productos_cotizacion = []
        self.tallas_seleccionadas = []
        self.con_igv = tk.BooleanVar(value=True)
        
        # Datos de la empresa
        self.datos_empresa = {
            'nombre': 'KARNIL COLLECTION',
            'direccion': 'Prolongación Huánuco 2069 - La Victoria, Lima - Perú',
            'telefono1': '997-900-022',
            'telefono2': '981-407-692',
            'email': 'ventas@karnilcorp.com',
            'instagram': '@karnilcollection',
            'facebook': 'Karnil KC'
        }
        
        self.crear_interfaz()
        self.cargar_ultima_cotizacion()
    
    def centrar_ventana(self, ancho, alto):
        """Centrar ventana en la pantalla"""
        pantalla_ancho = self.root.winfo_screenwidth()
        pantalla_alto = self.root.winfo_screenheight()
        x = (pantalla_ancho // 2) - (ancho // 2)
        y = (pantalla_alto // 2) - (alto // 2)
        self.root.geometry(f'{ancho}x{alto}+{x}+{y}')
    
    def cargar_ultima_cotizacion(self):
        """Cargar la última cotización del usuario actual"""
        try:
            conn = sqlite3.connect("karnil.db")
            c = conn.cursor()
            
            # Buscar la última cotización del usuario
            c.execute("""SELECT cliente_nombre, cliente_documento, cliente_tipo,
                                telefono, email, direccion 
                         FROM cotizaciones 
                         WHERE usuario_id = ? 
                         ORDER BY fecha DESC LIMIT 1""", (self.usuario['id'],))
            
            ultima_cotizacion = c.fetchone()
            
            if ultima_cotizacion:
                # Cargar datos del cliente
                campos_cliente = ['nombre_completo', 'n_documento', 'tipo_documento', 
                                 'teléfono', 'email', 'dirección']
                
                for campo, valor in zip(campos_cliente, ultima_cotizacion):
                    if valor and campo in self.entradas_cliente:
                        widget = self.entradas_cliente[campo]
                        if isinstance(widget, tk.Entry):
                            widget.delete(0, tk.END)
                            widget.insert(0, valor)
                        elif isinstance(widget, ttk.Combobox):
                            widget.set(valor)
            
            conn.close()
        except Exception as e:
            print(f"Error al cargar última cotización: {e}")
    
    def crear_interfaz(self):
        """Crear la interfaz gráfica"""
        top_frame = tk.Frame(self.root, bg=self.color_verde_oscuro, height=70)
        top_frame.pack(fill=tk.X)
        top_frame.pack_propagate(False)
        
        tk.Label(top_frame, text="KARNIL COLLECTION", 
                font=("Arial", 20, "bold"), 
                bg=self.color_verde_oscuro, fg="white").pack(side=tk.LEFT, padx=30, pady=15)
        
        tk.Label(top_frame, text=f"Usuario: {self.usuario['nombre']} | {self.usuario['rol'].upper()}", 
                font=("Arial", 11), 
                bg=self.color_verde_oscuro, fg=self.color_verde_claro).pack(side=tk.LEFT, padx=10, pady=15)
        
        tk.Button(top_frame, text="Cerrar Sesión", bg=self.color_verde_claro, fg="black",
                 font=("Arial", 10), command=self.cerrar_sesion).pack(side=tk.RIGHT, padx=20, pady=15)
        
        if self.usuario['rol'] == 'admin':
            tk.Button(top_frame, text="📦 Gestionar Productos", bg="#3498DB", fg="white",
                     font=("Arial", 10), command=self.gestionar_productos).pack(side=tk.RIGHT, padx=10, pady=15)
        
        tk.Button(top_frame, text="📋 Historial de Cotizaciones", bg="#9B59B6", fg="white",
                 font=("Arial", 10), command=self.ver_historial_cotizaciones).pack(side=tk.RIGHT, padx=10, pady=15)
        
        main_container = tk.Frame(self.root, bg=self.color_gris_claro)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        left_panel = tk.LabelFrame(main_container, text="📋 INFORMACIÓN DEL CLIENTE", 
                                  font=("Arial", 12, "bold"),
                                  bg="white", fg=self.color_verde_oscuro,
                                  relief=tk.RIDGE, borderwidth=2)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        right_panel = tk.LabelFrame(main_container, text="🛒 PRODUCTOS Y TOTALES", 
                                   font=("Arial", 12, "bold"),
                                   bg="white", fg=self.color_verde_oscuro,
                                   relief=tk.RIDGE, borderwidth=2)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        cliente_frame = tk.Frame(left_panel, bg="white", padx=20, pady=20)
        cliente_frame.pack(fill=tk.BOTH, expand=True)
        
        campos = [
            ("Nombre Completo:", "entry_largo"),
            ("Tipo Documento:", ["DNI", "RUC", "CE", "Pasaporte"]),
            ("N° Documento:", "entry"),
            ("Teléfono:", "entry"),
            ("Email:", "entry_largo"),
            ("Dirección:", "entry_largo")
        ]
        
        self.entradas_cliente = {}
        
        for i, (label, tipo) in enumerate(campos):
            tk.Label(cliente_frame, text=label, bg="white", 
                    font=("Arial", 10)).grid(row=i, column=0, sticky='w', pady=8, padx=5)
            
            if isinstance(tipo, list):
                var = tk.StringVar()
                combo = ttk.Combobox(cliente_frame, textvariable=var, 
                                    values=tipo, width=27, state="readonly")
                combo.grid(row=i, column=1, pady=8, padx=5)
                key = label.lower().replace(" ", "_").replace("°", "").replace(":", "")
                self.entradas_cliente[key] = combo
            elif tipo == "entry_largo":
                entry = tk.Entry(cliente_frame, width=35, font=("Arial", 10))
                entry.grid(row=i, column=1, pady=8, padx=5)
                key = label.lower().replace(" ", "_").replace(":", "")
                self.entradas_cliente[key] = entry
            else:
                entry = tk.Entry(cliente_frame, width=25, font=("Arial", 10))
                entry.grid(row=i, column=1, pady=8, padx=5)
                key = label.lower().replace(" ", "_").replace("°", "").replace(":", "")
                self.entradas_cliente[key] = entry
        
        tk.Frame(cliente_frame, height=2, bg="#ECF0F1").grid(row=len(campos), column=0, columnspan=2, sticky='ew', pady=15)
        
        producto_frame = tk.Frame(cliente_frame, bg="white")
        producto_frame.grid(row=len(campos)+1, column=0, columnspan=2, sticky='ew', pady=10)
        
        tk.Label(producto_frame, text="Agregar Producto:", bg="white", 
                font=("Arial", 11, "bold")).pack(anchor='w', pady=5)
        
        frame_datos_producto = tk.Frame(producto_frame, bg="white")
        frame_datos_producto.pack(fill=tk.X, pady=5)
        
        tk.Label(frame_datos_producto, text="Nombre del Producto:", bg="white").pack(anchor='w')
        self.entry_nombre_producto = tk.Entry(frame_datos_producto, width=40, font=("Arial", 10))
        self.entry_nombre_producto.pack(fill=tk.X, pady=2)
        
        frame_material = tk.Frame(producto_frame, bg="white")
        frame_material.pack(fill=tk.X, pady=5)
        
        tk.Label(frame_material, text="Material:", bg="white").pack(side=tk.LEFT, anchor='w', padx=(0, 10))
        self.entry_material = tk.Entry(frame_material, width=30)
        self.entry_material.pack(side=tk.LEFT)
        
        frame_precios_base = tk.Frame(producto_frame, bg="white")
        frame_precios_base.pack(fill=tk.X, pady=5)
        
        tk.Label(frame_precios_base, text="Precio Base S/:", bg="white").pack(side=tk.LEFT, anchor='w', padx=(0, 10))
        self.entry_precio_base = tk.Entry(frame_precios_base, width=12)
        self.entry_precio_base.pack(side=tk.LEFT, padx=(0, 20))
        
        tk.Label(frame_precios_base, text="Precio x Mayor S/:", bg="white").pack(side=tk.LEFT, anchor='w', padx=(0, 10))
        self.entry_precio_mayor = tk.Entry(frame_precios_base, width=12)
        self.entry_precio_mayor.pack(side=tk.LEFT)
        
        tk.Button(producto_frame, text="👕 Gestionar Tallas y Colores", bg="#9B59B6", fg="white",
                 font=("Arial", 10, "bold"), command=self.abrir_dialogo_tallas_colores,
                 width=25).pack(pady=10)
        
        self.lbl_tallas_seleccionadas = tk.Label(producto_frame, text="Tallas: Ninguna", 
                                                bg="white", fg="#7F8C8D", font=("Arial", 9))
        self.lbl_tallas_seleccionadas.pack(pady=5)
        
        tk.Button(producto_frame, text="➕ Agregar Producto a Cotización", bg=self.color_verde, fg="white",
                 font=("Arial", 10, "bold"), command=self.agregar_producto_cotizacion,
                 width=30).pack(pady=15)
        
        tabla_frame = tk.Frame(right_panel, bg="white")
        tabla_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        columns = ("#", "Producto", "Talla", "Cant", "Color", "Material", "Precio S/", "Subtotal S/")
        self.tree_productos = ttk.Treeview(tabla_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.tree_productos.heading(col, text=col)
        
        self.tree_productos.column("#", width=40, anchor='center')
        self.tree_productos.column("Producto", width=180)
        self.tree_productos.column("Talla", width=60, anchor='center')
        self.tree_productos.column("Cant", width=50, anchor='center')
        self.tree_productos.column("Color", width=70, anchor='center')
        self.tree_productos.column("Material", width=100, anchor='center')
        self.tree_productos.column("Precio S/", width=80, anchor='e')
        self.tree_productos.column("Subtotal S/", width=90, anchor='e')
        
        scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tree_productos.yview)
        self.tree_productos.configure(yscrollcommand=scrollbar.set)
        
        self.tree_productos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        btn_frame_productos = tk.Frame(tabla_frame, bg="white")
        btn_frame_productos.pack(pady=10)
        
        tk.Button(btn_frame_productos, text="🗑️ Eliminar Seleccionado", bg=self.color_rojo, fg="white",
                 command=self.eliminar_producto).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame_productos, text="🧹 Limpiar Todo", bg="#F39C12", fg="white",
                 command=self.limpiar_todo).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame_productos, text="✏️ Editar Producto", bg="#3498DB", fg="white",
                 command=self.editar_producto_seleccionado, width=15).pack(side=tk.LEFT, padx=5)
        
        totales_frame = tk.Frame(right_panel, bg="white", padx=20, pady=10)
        totales_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        igv_frame = tk.Frame(totales_frame, bg="white")
        igv_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(igv_frame, text="Incluir IGV (18%):", bg="white", 
                font=("Arial", 10)).pack(side=tk.LEFT)
        
        self.check_igv = tk.Checkbutton(igv_frame, variable=self.con_igv, 
                                       command=self.calcular_totales,
                                       bg="white")
        self.check_igv.pack(side=tk.LEFT, padx=10)
        self.check_igv.select()
        
        tk.Label(igv_frame, text="Seleccione si la cotización incluye IGV", 
                bg="white", font=("Arial", 9), fg="#7F8C8D").pack(side=tk.LEFT)
        
        self.lbl_subtotal = tk.Label(totales_frame, text="Subtotal: S/0.00", 
                                    font=("Arial", 11), bg="white", anchor='w')
        self.lbl_subtotal.pack(fill=tk.X, pady=3)
        
        self.lbl_igv = tk.Label(totales_frame, text="IGV (18%): S/0.00", 
                               font=("Arial", 11), bg="white", anchor='w')
        self.lbl_igv.pack(fill=tk.X, pady=3)
        
        self.lbl_total = tk.Label(totales_frame, text="TOTAL: S/0.00", 
                                 font=("Arial", 14, "bold"), bg="white",
                                 fg=self.color_verde_oscuro, anchor='w')
        self.lbl_total.pack(fill=tk.X, pady=10)
        
        tk.Frame(totales_frame, height=2, bg="#ECF0F1").pack(fill=tk.X, pady=10)
        
        accion_frame = tk.Frame(totales_frame, bg="white")
        accion_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(accion_frame, text="💾 Guardar Cotización", bg=self.color_verde_oscuro, fg="white",
                 font=("Arial", 11, "bold"), command=self.guardar_cotizacion,
                 width=20).pack(side=tk.LEFT, padx=5)
        
        tk.Button(accion_frame, text="📄 Exportar PDF", bg="#E74C3C", fg="white",
                 font=("Arial", 11), command=self.exportar_pdf,
                 width=15).pack(side=tk.LEFT, padx=5)
        
        tk.Button(accion_frame, text="📊 Exportar Excel", bg="#3498DB", fg="white",
                 font=("Arial", 11), command=self.exportar_excel,
                 width=15).pack(side=tk.LEFT, padx=5)
        
        tk.Button(accion_frame, text="🔄 Nueva", bg="#9B59B6", fg="white",
                 font=("Arial", 11), command=self.nueva_cotizacion,
                 width=12).pack(side=tk.LEFT, padx=5)
    
    def cerrar_sesion(self):
        """Cerrar sesión y volver al login"""
        if messagebox.askyesno("Cerrar Sesión", "¿Está seguro de cerrar sesión?"):
            for widget in self.root.winfo_children():
                widget.destroy()
            SistemaLogin(self.root)
    
    def abrir_dialogo_tallas_colores(self):
        """Abrir diálogo para gestionar tallas y colores"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Gestionar Tallas y Colores")
        dialog.geometry("600x500")
        dialog.configure(bg="white")
        dialog.transient(self.root)
        dialog.grab_set()
        
        dialog.update_idletasks()
        ancho = dialog.winfo_width()
        alto = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (ancho // 2)
        y = (dialog.winfo_screenheight() // 2) - (alto // 2)
        dialog.geometry(f'{ancho}x{alto}+{x}+{y}')
        
        tk.Label(dialog, text="👕 GESTIONAR TALLAS Y COLORES", 
                font=("Arial", 14, "bold"), bg="white", fg=self.color_verde_oscuro).pack(pady=10)
        
        controles_frame = tk.Frame(dialog, bg="white", padx=20, pady=10)
        controles_frame.pack(fill=tk.BOTH, expand=True)
        
        nueva_talla_frame = tk.Frame(controles_frame, bg="white")
        nueva_talla_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(nueva_talla_frame, text="Nueva Talla:", bg="white").pack(side=tk.LEFT, padx=(0, 5))
        entry_nueva_talla = tk.Entry(nueva_talla_frame, width=10)
        entry_nueva_talla.pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Label(nueva_talla_frame, text="Cantidad:", bg="white").pack(side=tk.LEFT, padx=(0, 5))
        entry_nueva_cantidad = tk.Entry(nueva_talla_frame, width=8)
        entry_nueva_cantidad.pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Label(nueva_talla_frame, text="Precio S/:", bg="white").pack(side=tk.LEFT, padx=(0, 5))
        entry_nuevo_precio = tk.Entry(nueva_talla_frame, width=10)
        entry_nuevo_precio.insert(0, self.entry_precio_base.get() or "0.00")
        entry_nuevo_precio.pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Label(nueva_talla_frame, text="Colores (separar por coma):", bg="white").pack(side=tk.LEFT, padx=(0, 5))
        entry_colores_talla = tk.Entry(nueva_talla_frame, width=20)
        entry_colores_talla.pack(side=tk.LEFT, padx=(0, 10))
        
        def agregar_talla():
            talla = entry_nueva_talla.get().strip()
            cantidad_str = entry_nueva_cantidad.get().strip()
            precio_str = entry_nuevo_precio.get().strip()
            colores_text = entry_colores_talla.get().strip()
            
            if not talla:
                messagebox.showerror("Error", "Ingrese una talla")
                return
            
            try:
                cantidad = int(cantidad_str) if cantidad_str else 1
                precio = float(precio_str) if precio_str else float(self.entry_precio_base.get() or 0)
            except ValueError:
                messagebox.showerror("Error", "Cantidad y precio deben ser números válidos")
                return
            
            colores_lista = []
            if colores_text:
                colores_lista = [c.strip() for c in colores_text.split(',') if c.strip()]
            
            self.tallas_seleccionadas.append({
                'talla': talla,
                'cantidad': cantidad,
                'precio': precio,
                'colores': colores_lista
            })
            
            self.actualizar_etiqueta_tallas()
            actualizar_lista_tallas()
            
            entry_nueva_talla.delete(0, tk.END)
            entry_nueva_cantidad.delete(0, tk.END)
            entry_nuevo_precio.delete(0, tk.END)
            entry_colores_talla.delete(0, tk.END)
        
        tk.Button(nueva_talla_frame, text="➕ Agregar", bg=self.color_verde, fg="white",
                 command=agregar_talla).pack(side=tk.LEFT)
        
        lista_frame = tk.Frame(controles_frame, bg="white")
        lista_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        columns = ("Talla", "Cantidad", "Precio S/", "Colores")
        tree_tallas = ttk.Treeview(lista_frame, columns=columns, show="headings", height=8)
        
        tree_tallas.heading("Talla", text="Talla")
        tree_tallas.heading("Cantidad", text="Cantidad")
        tree_tallas.heading("Precio S/", text="Precio S/")
        tree_tallas.heading("Colores", text="Colores")
        
        tree_tallas.column("Talla", width=80, anchor='center')
        tree_tallas.column("Cantidad", width=80, anchor='center')
        tree_tallas.column("Precio S/", width=80, anchor='center')
        tree_tallas.column("Colores", width=200)
        
        scrollbar = ttk.Scrollbar(lista_frame, orient="vertical", command=tree_tallas.yview)
        tree_tallas.configure(yscrollcommand=scrollbar.set)
        
        tree_tallas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        def actualizar_lista_tallas():
            for item in tree_tallas.get_children():
                tree_tallas.delete(item)
            
            for i, talla_info in enumerate(self.tallas_seleccionadas):
                colores_text = ", ".join(talla_info['colores']) if talla_info['colores'] else "Sin colores"
                tree_tallas.insert("", "end", values=(
                    talla_info['talla'],
                    talla_info['cantidad'],
                    f"{talla_info['precio']:.2f}",
                    colores_text
                ))
        
        def eliminar_talla():
            seleccion = tree_tallas.selection()
            if not seleccion:
                messagebox.showinfo("Eliminar", "Seleccione una talla para eliminar")
                return
            
            item = tree_tallas.item(seleccion[0])
            talla = item['values'][0]
            self.tallas_seleccionadas = [t for t in self.tallas_seleccionadas if t['talla'] != talla]
            actualizar_lista_tallas()
            self.actualizar_etiqueta_tallas()
        
        botones_frame = tk.Frame(controles_frame, bg="white")
        botones_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(botones_frame, text="🗑️ Eliminar Seleccionada", bg=self.color_rojo, fg="white",
                 command=eliminar_talla).pack(side=tk.LEFT, padx=5)
        
        tk.Button(botones_frame, text="💾 Guardar y Cerrar", bg=self.color_verde, fg="white",
                 command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
        
        actualizar_lista_tallas()
    
    def actualizar_etiqueta_tallas(self):
        """Actualizar la etiqueta que muestra las tallas seleccionadas"""
        if not self.tallas_seleccionadas:
            self.lbl_tallas_seleccionadas.config(text="Tallas: Ninguna", fg="#7F8C8D")
        else:
            tallas_text = ", ".join([t['talla'] for t in self.tallas_seleccionadas])
            self.lbl_tallas_seleccionadas.config(text=f"Tallas: {tallas_text}", fg=self.color_verde_oscuro)
    
    def agregar_producto_cotizacion(self):
        """Agregar producto con múltiples tallas a la cotización"""
        nombre_producto = self.entry_nombre_producto.get().strip()
        
        if not nombre_producto:
            messagebox.showerror("Error", "Ingrese el nombre del producto")
            return
        
        if not self.tallas_seleccionadas:
            messagebox.showerror("Error", "Debe agregar al menos una talla")
            return
        
        for talla_info in self.tallas_seleccionadas:
            if talla_info['cantidad'] <= 0:
                messagebox.showerror("Error", f"La talla {talla_info['talla']} debe tener cantidad mayor a 0")
                return
        
        material = self.entry_material.get().strip()
        
        for talla_info in self.tallas_seleccionadas:
            if talla_info['cantidad'] > 0:
                colores_talla = talla_info.get('colores', [])
                color_seleccionado = colores_talla[0] if colores_talla else ""
                subtotal_talla = talla_info['cantidad'] * talla_info['precio']
                
                producto_dict = {
                    'id': len(self.productos_cotizacion) + 1,
                    'nombre': nombre_producto,
                    'talla': talla_info['talla'],
                    'cantidad': talla_info['cantidad'],
                    'color': color_seleccionado,
                    'material': material,
                    'precio': talla_info['precio'],
                    'subtotal': subtotal_talla
                }
                
                self.productos_cotizacion.append(producto_dict)
                
                num = len(self.productos_cotizacion)
                self.tree_productos.insert("", "end", values=(
                    num,
                    producto_dict['nombre'][:30],
                    producto_dict['talla'],
                    producto_dict['cantidad'],
                    producto_dict['color'],
                    producto_dict['material'][:15] if producto_dict['material'] else "",
                    f"{producto_dict['precio']:.2f}",
                    f"{producto_dict['subtotal']:.2f}"
                ))
        
        self.calcular_totales()
        
        self.entry_nombre_producto.delete(0, tk.END)
        self.entry_material.delete(0, tk.END)
        self.entry_precio_base.delete(0, tk.END)
        self.entry_precio_mayor.delete(0, tk.END)
        self.tallas_seleccionadas = []
        self.actualizar_etiqueta_tallas()
        
        self.entry_nombre_producto.focus()
    
    def editar_producto_seleccionado(self):
        """Editar producto seleccionado en la tabla"""
        seleccion = self.tree_productos.selection()
        if not seleccion:
            messagebox.showinfo("Editar", "Seleccione un producto de la tabla para editar")
            return
        
        item = self.tree_productos.item(seleccion[0])
        valores = item['values']
        index = int(valores[0]) - 1
        
        if 0 <= index < len(self.productos_cotizacion):
            producto = self.productos_cotizacion[index]
            
            ventana_edicion = tk.Toplevel(self.root)
            ventana_edicion.title("Editar Producto")
            ventana_edicion.geometry("400x300")
            ventana_edicion.configure(bg="white")
            ventana_edicion.transient(self.root)
            ventana_edicion.grab_set()
            
            ventana_edicion.update_idletasks()
            ancho = ventana_edicion.winfo_width()
            alto = ventana_edicion.winfo_height()
            x = (ventana_edicion.winfo_screenwidth() // 2) - (ancho // 2)
            y = (ventana_edicion.winfo_screenheight() // 2) - (alto // 2)
            ventana_edicion.geometry(f'{ancho}x{alto}+{x}+{y}')
            
            tk.Label(ventana_edicion, text="✏️ EDITAR PRODUCTO", 
                    font=("Arial", 14, "bold"), bg="white", fg=self.color_verde_oscuro).pack(pady=10)
            
            campos_frame = tk.Frame(ventana_edicion, bg="white", padx=20, pady=10)
            campos_frame.pack(fill=tk.BOTH, expand=True)
            
            campos = [
                ("Nombre del Producto:", producto['nombre']),
                ("Talla:", producto['talla']),
                ("Cantidad:", str(producto['cantidad'])),
                ("Color:", producto['color']),
                ("Material:", producto['material']),
                ("Precio Unitario (S/):", str(producto['precio']))
            ]
            
            entries = {}
            for i, (label, valor) in enumerate(campos):
                tk.Label(campos_frame, text=label, bg="white", font=("Arial", 9)).grid(row=i, column=0, sticky='w', pady=5, padx=5)
                entry = tk.Entry(campos_frame, width=30, font=("Arial", 9))
                entry.insert(0, str(valor))
                entry.grid(row=i, column=1, pady=5, padx=5)
                key = label.split(":")[0].strip().lower().replace(" ", "_")
                entries[key] = entry
            
            btn_frame = tk.Frame(ventana_edicion, bg="white")
            btn_frame.pack(pady=20)
            
            def guardar_cambios():
                try:
                    nueva_cantidad = int(entries['cantidad'].get())
                    nuevo_precio = float(entries['precio_unitario_(s/)'].get())
                    
                    if nueva_cantidad <= 0 or nuevo_precio <= 0:
                        messagebox.showerror("Error", "Cantidad y precio deben ser mayores a 0")
                        return
                    
                    self.productos_cotizacion[index]['nombre'] = entries['nombre_del_producto'].get()
                    self.productos_cotizacion[index]['talla'] = entries['talla'].get()
                    self.productos_cotizacion[index]['cantidad'] = nueva_cantidad
                    self.productos_cotizacion[index]['color'] = entries['color'].get()
                    self.productos_cotizacion[index]['material'] = entries['material'].get()
                    self.productos_cotizacion[index]['precio'] = nuevo_precio
                    self.productos_cotizacion[index]['subtotal'] = nueva_cantidad * nuevo_precio
                    
                    nuevos_valores = (
                        index + 1,
                        entries['nombre_del_producto'].get()[:30],
                        entries['talla'].get(),
                        nueva_cantidad,
                        entries['color'].get(),
                        entries['material'].get()[:15] if entries['material'].get() else "",
                        f"{nuevo_precio:.2f}",
                        f"{(nueva_cantidad * nuevo_precio):.2f}"
                    )
                    self.tree_productos.item(seleccion[0], values=nuevos_valores)
                    
                    self.calcular_totales()
                    messagebox.showinfo("Éxito", "✅ Producto actualizado correctamente")
                    ventana_edicion.destroy()
                    
                except ValueError as e:
                    messagebox.showerror("Error", f"Datos inválidos: {str(e)}")
                except Exception as e:
                    messagebox.showerror("Error", f"Error al actualizar: {str(e)}")
            
            tk.Button(btn_frame, text="💾 Guardar Cambios", bg=self.color_verde, fg="white",
                     font=("Arial", 10, "bold"), command=guardar_cambios).pack(side=tk.LEFT, padx=10)
            
            tk.Button(btn_frame, text="❌ Cancelar", bg=self.color_rojo, fg="white",
                     font=("Arial", 10), command=ventana_edicion.destroy).pack(side=tk.LEFT, padx=10)
    
    def eliminar_producto(self):
        """Eliminar producto seleccionado"""
        seleccion = self.tree_productos.selection()
        if not seleccion:
            messagebox.showerror("Error", "Seleccione un producto para eliminar")
            return
        
        item = self.tree_productos.item(seleccion[0])
        index = int(item['values'][0]) - 1
        
        if 0 <= index < len(self.productos_cotizacion):
            del self.productos_cotizacion[index]
        
        self.tree_productos.delete(seleccion[0])
        
        for i, item_id in enumerate(self.tree_productos.get_children()):
            valores = list(self.tree_productos.item(item_id)['values'])
            valores[0] = i + 1
            self.tree_productos.item(item_id, values=valores)
        
        self.calcular_totales()
    
    def limpiar_todo(self):
        """Limpiar toda la cotización"""
        if not self.productos_cotizacion:
            return
        
        if messagebox.askyesno("Confirmar", "¿Está seguro de limpiar toda la cotización?"):
            self.productos_cotizacion = []
            for item in self.tree_productos.get_children():
                self.tree_productos.delete(item)
            self.calcular_totales()
    
    def calcular_totales(self):
        """Calcular subtotal, IGV y total según opción seleccionada"""
        subtotal = sum(p['subtotal'] for p in self.productos_cotizacion)
        
        if self.con_igv.get():
            igv = subtotal * 0.18
            total = subtotal + igv
            self.lbl_igv.config(text=f"IGV (18%): S/{igv:.2f}")
            self.lbl_total.config(text=f"TOTAL (con IGV): S/{total:.2f}")
        else:
            igv = 0
            total = subtotal
            self.lbl_igv.config(text="IGV: NO APLICA")
            self.lbl_total.config(text=f"TOTAL (sin IGV): S/{total:.2f}")
        
        self.lbl_subtotal.config(text=f"Subtotal: S/{subtotal:.2f}")
    
    def gestionar_productos(self):
        """Gestionar productos (solo para administrador)"""
        ventana_gestion = tk.Toplevel(self.root)
        ventana_gestion.title("Gestión de Productos")
        ventana_gestion.geometry("1000x600")
        ventana_gestion.configure(bg="white")
        ventana_gestion.transient(self.root)
        
        ventana_gestion.update_idletasks()
        ancho = ventana_gestion.winfo_width()
        alto = ventana_gestion.winfo_height()
        x = (ventana_gestion.winfo_screenwidth() // 2) - (ancho // 2)
        y = (ventana_gestion.winfo_screenheight() // 2) - (alto // 2)
        ventana_gestion.geometry(f'{ancho}x{alto}+{x}+{y}')
        
        tk.Label(ventana_gestion, text="📦 GESTIÓN DE PRODUCTOS", 
                font=("Arial", 16, "bold"), bg="white", fg=self.color_verde_oscuro).pack(pady=10)
        
        busqueda_frame = tk.Frame(ventana_gestion, bg="white", padx=20, pady=10)
        busqueda_frame.pack(fill=tk.X)
        
        tk.Label(busqueda_frame, text="Buscar:", bg="white").pack(side=tk.LEFT, padx=(0, 5))
        entry_buscar = tk.Entry(busqueda_frame, width=30, font=("Arial", 10))
        entry_buscar.pack(side=tk.LEFT, padx=(0, 10))
        
        def buscar():
            termino = entry_buscar.get().strip()
            cargar_productos(termino)
        
        tk.Button(busqueda_frame, text="🔍 Buscar", bg=self.color_verde_claro, fg="black",
                 command=buscar).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(busqueda_frame, text="➕ Nuevo Producto", bg=self.color_verde, fg="white",
                 command=lambda: self.crear_ventana_nuevo_producto(cargar_productos)).pack(side=tk.LEFT)
        
        frame_tabla = tk.Frame(ventana_gestion, bg="white", padx=20, pady=10)
        frame_tabla.pack(fill=tk.BOTH, expand=True)
        
        columns = ("ID", "Código", "Nombre", "Precio Base", "Precio Mayor", "Tallas", "Colores", "Material")
        tree_productos = ttk.Treeview(frame_tabla, columns=columns, show="headings", height=15)
        
        for col in columns:
            tree_productos.heading(col, text=col)
        
        tree_productos.column("ID", width=50)
        tree_productos.column("Código", width=80)
        tree_productos.column("Nombre", width=200)
        tree_productos.column("Precio Base", width=90, anchor='e')
        tree_productos.column("Precio Mayor", width=90, anchor='e')
        tree_productos.column("Tallas", width=150)
        tree_productos.column("Colores", width=150)
        tree_productos.column("Material", width=120)
        
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tree_productos.yview)
        tree_productos.configure(yscrollcommand=scrollbar.set)
        
        tree_productos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        def cargar_productos(termino=""):
            for item in tree_productos.get_children():
                tree_productos.delete(item)
            
            conn = sqlite3.connect("karnil.db")
            c = conn.cursor()
            
            if termino:
                c.execute("""SELECT id, codigo, nombre, precio_base, precio_mayor, 
                            tallas_cantidades, colores_disponibles, tipo_material 
                            FROM productos 
                            WHERE codigo LIKE ? OR nombre LIKE ? 
                            ORDER BY codigo""", 
                         (f'%{termino}%', f'%{termino}%'))
            else:
                c.execute("""SELECT id, codigo, nombre, precio_base, precio_mayor, 
                            tallas_cantidades, colores_disponibles, tipo_material 
                            FROM productos 
                            ORDER BY codigo""")
            
            productos = c.fetchall()
            conn.close()
            
            for producto in productos:
                tallas_cantidades = json.loads(producto[5]) if producto[5] else {}
                tallas_text = ", ".join(tallas_cantidades.keys()) if tallas_cantidades else "Sin tallas"
                
                colores = json.loads(producto[6]) if producto[6] else []
                colores_text = ", ".join(colores) if colores else "Sin colores"
                
                tree_productos.insert("", "end", values=(
                    producto[0],
                    producto[1],
                    producto[2],
                    f"{producto[3]:.2f}",
                    f"{producto[4]:.2f}",
                    tallas_text,
                    colores_text,
                    producto[7]
                ))
        
        def editar_producto():
            seleccion = tree_productos.selection()
            if not seleccion:
                messagebox.showinfo("Editar", "Seleccione un producto para editar")
                return
            
            item = tree_productos.item(seleccion[0])
            producto_id = item['values'][0]
            
            conn = sqlite3.connect("karnil.db")
            c = conn.cursor()
            c.execute("""SELECT codigo, nombre, precio_base, precio_mayor, 
                        tallas_cantidades, precios_tallas, colores_tallas, 
                        colores_disponibles, tipo_material 
                        FROM productos WHERE id = ?""", (producto_id,))
            
            producto = c.fetchone()
            conn.close()
            
            if producto:
                self.crear_ventana_editar_producto(producto_id, producto, cargar_productos)
        
        def eliminar_producto():
            seleccion = tree_productos.selection()
            if not seleccion:
                messagebox.showinfo("Eliminar", "Seleccione un producto para eliminar")
                return
            
            item = tree_productos.item(seleccion[0])
            producto_id = item['values'][0]
            producto_nombre = item['values'][2]
            
            if messagebox.askyesno("Confirmar", 
                                  f"¿Está seguro de eliminar el producto:\n{producto_nombre}?"):
                conn = sqlite3.connect("karnil.db")
                c = conn.cursor()
                c.execute("DELETE FROM productos WHERE id = ?", (producto_id,))
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Éxito", "Producto eliminado correctamente")
                cargar_productos()
        
        botones_frame = tk.Frame(ventana_gestion, bg="white", pady=10)
        botones_frame.pack(fill=tk.X)
        
        tk.Button(botones_frame, text="✏️ Editar Seleccionado", bg="#3498DB", fg="white",
                 command=editar_producto).pack(side=tk.LEFT, padx=20)
        
        tk.Button(botones_frame, text="🗑️ Eliminar Seleccionado", bg=self.color_rojo, fg="white",
                 command=eliminar_producto).pack(side=tk.LEFT, padx=20)
        
        tk.Button(botones_frame, text="🔄 Actualizar", bg="#9B59B6", fg="white",
                 command=lambda: cargar_productos()).pack(side=tk.LEFT, padx=20)
        
        tk.Button(botones_frame, text="❌ Cerrar", bg="#7F8C8D", fg="white",
                 command=ventana_gestion.destroy).pack(side=tk.RIGHT, padx=20)
        
        cargar_productos()
    
    def crear_ventana_nuevo_producto(self, callback_actualizar=None):
        """Crear ventana para nuevo producto"""
        ventana_nuevo = tk.Toplevel(self.root)
        ventana_nuevo.title("Nuevo Producto")
        ventana_nuevo.geometry("600x500")
        ventana_nuevo.configure(bg="white")
        ventana_nuevo.transient(self.root)
        ventana_nuevo.grab_set()
        
        ventana_nuevo.update_idletasks()
        ancho = ventana_nuevo.winfo_width()
        alto = ventana_nuevo.winfo_height()
        x = (ventana_nuevo.winfo_screenwidth() // 2) - (ancho // 2)
        y = (ventana_nuevo.winfo_screenheight() // 2) - (alto // 2)
        ventana_nuevo.geometry(f'{ancho}x{alto}+{x}+{y}')
        
        tk.Label(ventana_nuevo, text="➕ NUEVO PRODUCTO", 
                font=("Arial", 14, "bold"), bg="white", fg=self.color_verde_oscuro).pack(pady=10)
        
        campos_frame = tk.Frame(ventana_nuevo, bg="white", padx=30, pady=10)
        campos_frame.pack(fill=tk.BOTH, expand=True)
        
        campos = [
            ("Código:", "entry"),
            ("Nombre:", "entry_largo"),
            ("Precio Base S/:", "entry"),
            ("Precio x Mayor S/:", "entry"),
            ("Colores generales (separados por coma):", "entry_largo"),
            ("Tipo de Material:", "entry_largo")
        ]
        
        entries = {}
        for i, (label, tipo) in enumerate(campos):
            tk.Label(campos_frame, text=label, bg="white", font=("Arial", 9)).grid(row=i, column=0, sticky='w', pady=8, padx=5)
            
            if tipo == "entry_largo":
                entry = tk.Entry(campos_frame, width=40, font=("Arial", 9))
                entry.grid(row=i, column=1, pady=8, padx=5)
            else:
                entry = tk.Entry(campos_frame, width=20, font=("Arial", 9))
                entry.grid(row=i, column=1, pady=8, padx=5, sticky='w')
            
            key = label.split(":")[0].strip().lower().replace(" ", "_")
            entries[key] = entry
        
        tk.Label(campos_frame, text="Tallas (formato 'Talla:Cantidad:Precio:Colores'):", 
                bg="white", font=("Arial", 9)).grid(row=len(campos), column=0, sticky='w', pady=8, padx=5)
        
        entry_tallas = tk.Entry(campos_frame, width=40, font=("Arial", 9))
        entry_tallas.grid(row=len(campos), column=1, pady=8, padx=5)
        entry_tallas.insert(0, "S:10:45.00:Blanco,Azul, M:15:45.00:Azul,Negro")
        
        tk.Label(campos_frame, text="Nota: Separar diferentes tallas con coma", 
                bg="white", font=("Arial", 8), fg="#7F8C8D").grid(row=len(campos)+1, column=1, sticky='w', pady=2, padx=5)
        
        botones_frame = tk.Frame(ventana_nuevo, bg="white", pady=20)
        botones_frame.pack()
        
        def guardar_producto():
            try:
                codigo = entries['código'].get().strip()
                nombre = entries['nombre'].get().strip()
                
                if not codigo or not nombre:
                    messagebox.showerror("Error", "Código y Nombre son obligatorios")
                    return
                
                precio_base = float(entries['precio_base_s/'].get() or 0)
                precio_mayor = float(entries['precio_x_mayor_s/'].get() or 0)
                colores_generales = entries['colores_generales_(separados_por_coma)'].get().strip()
                material = entries['tipo_de_material'].get().strip()
                
                colores_lista = []
                if colores_generales:
                    colores_lista = [c.strip() for c in colores_generales.split(',') if c.strip()]
                
                tallas_text = entry_tallas.get().strip()
                tallas_cantidades = {}
                precios_tallas = {}
                colores_tallas = {}
                
                if tallas_text:
                    tallas_items = [item.strip() for item in tallas_text.split(',')]
                    for item in tallas_items:
                        if item:
                            partes = item.strip().split(':')
                            if len(partes) >= 3:
                                talla = partes[0].strip()
                                cantidad = int(partes[1].strip())
                                precio = float(partes[2].strip())
                                tallas_cantidades[talla] = cantidad
                                precios_tallas[talla] = precio
                                
                                if len(partes) >= 4:
                                    colores_talla = [c.strip() for c in partes[3].split(',') if c.strip()]
                                    colores_tallas[talla] = colores_talla
                
                tallas_cantidades_json = json.dumps(tallas_cantidades) if tallas_cantidades else "{}"
                precios_tallas_json = json.dumps(precios_tallas) if precios_tallas else "{}"
                colores_tallas_json = json.dumps(colores_tallas) if colores_tallas else "{}"
                colores_disponibles_json = json.dumps(colores_lista) if colores_lista else "[]"
                
                conn = sqlite3.connect("karnil.db")
                c = conn.cursor()
                
                c.execute("""INSERT INTO productos 
                          (codigo, nombre, precio_base, precio_mayor, tallas_cantidades, 
                           precios_tallas, colores_tallas, colores_disponibles, tipo_material)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                         (codigo, nombre, precio_base, precio_mayor, tallas_cantidades_json,
                          precios_tallas_json, colores_tallas_json, colores_disponibles_json, material))
                
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Éxito", "✅ Producto guardado correctamente")
                ventana_nuevo.destroy()
                
                if callback_actualizar:
                    callback_actualizar()
                
            except ValueError as e:
                messagebox.showerror("Error", f"Datos inválidos: {str(e)}")
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "El código ya existe")
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar: {str(e)}")
        
        tk.Button(botones_frame, text="💾 Guardar Producto", bg=self.color_verde, fg="white",
                 font=("Arial", 10, "bold"), command=guardar_producto).pack(side=tk.LEFT, padx=10)
        
        tk.Button(botones_frame, text="❌ Cancelar", bg=self.color_rojo, fg="white",
                 font=("Arial", 10), command=ventana_nuevo.destroy).pack(side=tk.LEFT, padx=10)
    
    def crear_ventana_editar_producto(self, producto_id, producto, callback_actualizar=None):
        """Crear ventana para editar producto"""
        ventana_editar = tk.Toplevel(self.root)
        ventana_editar.title("Editar Producto")
        ventana_editar.geometry("600x500")
        ventana_editar.configure(bg="white")
        ventana_editar.transient(self.root)
        ventana_editar.grab_set()
        
        ventana_editar.update_idletasks()
        ancho = ventana_editar.winfo_width()
        alto = ventana_editar.winfo_height()
        x = (ventana_editar.winfo_screenwidth() // 2) - (ancho // 2)
        y = (ventana_editar.winfo_screenheight() // 2) - (alto // 2)
        ventana_editar.geometry(f'{ancho}x{alto}+{x}+{y}')
        
        tk.Label(ventana_editar, text="✏️ EDITAR PRODUCTO", 
                font=("Arial", 14, "bold"), bg="white", fg=self.color_verde_oscuro).pack(pady=10)
        
        campos_frame = tk.Frame(ventana_editar, bg="white", padx=30, pady=10)
        campos_frame.pack(fill=tk.BOTH, expand=True)
        
        tallas_cantidades = json.loads(producto[4]) if producto[4] and producto[4] != '{}' else {}
        precios_tallas = json.loads(producto[5]) if producto[5] and producto[5] != '{}' else {}
        colores_tallas = json.loads(producto[6]) if producto[6] and producto[6] != '{}' else {}
        colores_disponibles = json.loads(producto[7]) if producto[7] and producto[7] != '[]' else []
        
        tallas_text = ""
        for talla, cantidad in tallas_cantidades.items():
            precio = precios_tallas.get(talla, producto[2])
            colores = colores_tallas.get(talla, [])
            colores_str = ",".join(colores)
            tallas_text += f"{talla}:{cantidad}:{precio}:{colores_str}, "
        
        tallas_text = tallas_text.rstrip(", ")
        colores_generales_str = ",".join(colores_disponibles)
        
        campos = [
            ("Código:", producto[0]),
            ("Nombre:", producto[1]),
            ("Precio Base S/:", str(producto[2])),
            ("Precio x Mayor S/:", str(producto[3])),
            ("Colores generales (separados por coma):", colores_generales_str),
            ("Tipo de Material:", producto[8] or "")
        ]
        
        entries = {}
        for i, (label, valor) in enumerate(campos):
            tk.Label(campos_frame, text=label, bg="white", font=("Arial", 9)).grid(row=i, column=0, sticky='w', pady=8, padx=5)
            
            entry = tk.Entry(campos_frame, width=40, font=("Arial", 9))
            entry.insert(0, str(valor))
            entry.grid(row=i, column=1, pady=8, padx=5)
            
            key = label.split(":")[0].strip().lower().replace(" ", "_")
            entries[key] = entry
        
        tk.Label(campos_frame, text="Tallas (formato 'Talla:Cantidad:Precio:Colores'):", 
                bg="white", font=("Arial", 9)).grid(row=len(campos), column=0, sticky='w', pady=8, padx=5)
        
        entry_tallas = tk.Entry(campos_frame, width=40, font=("Arial", 9))
        entry_tallas.insert(0, tallas_text)
        entry_tallas.grid(row=len(campos), column=1, pady=8, padx=5)
        
        tk.Label(campos_frame, text="Nota: Separar diferentes tallas con coma", 
                bg="white", font=("Arial", 8), fg="#7F8C8D").grid(row=len(campos)+1, column=1, sticky='w', pady=2, padx=5)
        
        botones_frame = tk.Frame(ventana_editar, bg="white", pady=20)
        botones_frame.pack()
        
        def actualizar_producto():
            try:
                codigo = entries['código'].get().strip()
                nombre = entries['nombre'].get().strip()
                precio_base = float(entries['precio_base_s/'].get() or 0)
                precio_mayor = float(entries['precio_x_mayor_s/'].get() or 0)
                colores_generales = entries['colores_generales_(separados_por_coma)'].get().strip()
                material = entries['tipo_de_material'].get().strip()
                
                colores_lista = []
                if colores_generales:
                    colores_lista = [c.strip() for c in colores_generales.split(',') if c.strip()]
                
                tallas_text = entry_tallas.get().strip()
                tallas_cantidades = {}
                precios_tallas = {}
                colores_tallas = {}
                
                if tallas_text:
                    tallas_items = [item.strip() for item in tallas_text.split(',')]
                    for item in tallas_items:
                        if item:
                            partes = item.strip().split(':')
                            if len(partes) >= 3:
                                talla = partes[0].strip()
                                cantidad = int(partes[1].strip())
                                precio = float(partes[2].strip())
                                tallas_cantidades[talla] = cantidad
                                precios_tallas[talla] = precio
                                
                                if len(partes) >= 4:
                                    colores_talla = [c.strip() for c in partes[3].split(',') if c.strip()]
                                    colores_tallas[talla] = colores_talla
                
                tallas_cantidades_json = json.dumps(tallas_cantidades) if tallas_cantidades else "{}"
                precios_tallas_json = json.dumps(precios_tallas) if precios_tallas else "{}"
                colores_tallas_json = json.dumps(colores_tallas) if colores_tallas else "{}"
                colores_disponibles_json = json.dumps(colores_lista) if colores_lista else "[]"
                
                conn = sqlite3.connect("karnil.db")
                c = conn.cursor()
                
                c.execute("""UPDATE productos 
                          SET codigo = ?, nombre = ?, precio_base = ?, precio_mayor = ?,
                              tallas_cantidades = ?, precios_tallas = ?, colores_tallas = ?,
                              colores_disponibles = ?, tipo_material = ?,
                              fecha_modificacion = CURRENT_TIMESTAMP
                          WHERE id = ?""",
                         (codigo, nombre, precio_base, precio_mayor, tallas_cantidades_json,
                          precios_tallas_json, colores_tallas_json, colores_disponibles_json, material, producto_id))
                
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Éxito", "✅ Producto actualizado correctamente")
                ventana_editar.destroy()
                
                if callback_actualizar:
                    callback_actualizar()
                
            except ValueError as e:
                messagebox.showerror("Error", f"Datos inválidos: {str(e)}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al actualizar: {str(e)}")
        
        tk.Button(botones_frame, text="💾 Guardar Cambios", bg=self.color_verde, fg="white",
                 font=("Arial", 10, "bold"), command=actualizar_producto).pack(side=tk.LEFT, padx=10)
        
        tk.Button(botones_frame, text="❌ Cancelar", bg=self.color_rojo, fg="white",
                 font=("Arial", 10), command=ventana_editar.destroy).pack(side=tk.LEFT, padx=10)
    
    def ver_historial_cotizaciones(self):
        """Ver historial de cotizaciones guardadas"""
        ventana_historial = tk.Toplevel(self.root)
        ventana_historial.title("📋 Historial de Cotizaciones")
        ventana_historial.geometry("1200x700")
        ventana_historial.configure(bg="white")
        ventana_historial.transient(self.root)
        
        ventana_historial.update_idletasks()
        ancho = ventana_historial.winfo_width()
        alto = ventana_historial.winfo_height()
        x = (ventana_historial.winfo_screenwidth() // 2) - (ancho // 2)
        y = (ventana_historial.winfo_screenheight() // 2) - (alto // 2)
        ventana_historial.geometry(f'{ancho}x{alto}+{x}+{y}')
        
        tk.Label(ventana_historial, text="📋 HISTORIAL DE COTIZACIONES", 
                font=("Arial", 16, "bold"), bg="white", fg=self.color_verde_oscuro).pack(pady=10)
        
        busqueda_frame = tk.Frame(ventana_historial, bg="white", padx=20, pady=10)
        busqueda_frame.pack(fill=tk.X)
        
        tk.Label(busqueda_frame, text="Buscar:", bg="white").pack(side=tk.LEFT, padx=(0, 5))
        entry_buscar = tk.Entry(busqueda_frame, width=30, font=("Arial", 10))
        entry_buscar.pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Label(busqueda_frame, text="Fecha desde:", bg="white").pack(side=tk.LEFT, padx=(20, 5))
        entry_fecha_desde = tk.Entry(busqueda_frame, width=12, font=("Arial", 10))
        entry_fecha_desde.pack(side=tk.LEFT, padx=(0, 5))
        entry_fecha_desde.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        tk.Label(busqueda_frame, text="Fecha hasta:", bg="white").pack(side=tk.LEFT, padx=(10, 5))
        entry_fecha_hasta = tk.Entry(busqueda_frame, width=12, font=("Arial", 10))
        entry_fecha_hasta.pack(side=tk.LEFT, padx=(0, 10))
        entry_fecha_hasta.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        def buscar_historial():
            termino = entry_buscar.get().strip()
            fecha_desde = entry_fecha_desde.get().strip()
            fecha_hasta = entry_fecha_hasta.get().strip()
            cargar_cotizaciones(termino, fecha_desde, fecha_hasta)
        
        tk.Button(busqueda_frame, text="🔍 Buscar", bg=self.color_verde_claro, fg="black",
                 command=buscar_historial).pack(side=tk.LEFT, padx=(0, 10))
        
        frame_tabla = tk.Frame(ventana_historial, bg="white", padx=20, pady=10)
        frame_tabla.pack(fill=tk.BOTH, expand=True)
        
        columns = ("N°", "Fecha", "Cliente", "Documento", "Teléfono", "Subtotal", "IGV", "Total", "Estado")
        tree_cotizaciones = ttk.Treeview(frame_tabla, columns=columns, show="headings", height=15)
        
        for col in columns:
            tree_cotizaciones.heading(col, text=col)
        
        tree_cotizaciones.column("N°", width=100)
        tree_cotizaciones.column("Fecha", width=120)
        tree_cotizaciones.column("Cliente", width=150)
        tree_cotizaciones.column("Documento", width=100)
        tree_cotizaciones.column("Teléfono", width=100)
        tree_cotizaciones.column("Subtotal", width=90, anchor='e')
        tree_cotizaciones.column("IGV", width=80, anchor='e')
        tree_cotizaciones.column("Total", width=90, anchor='e')
        tree_cotizaciones.column("Estado", width=80, anchor='center')
        
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tree_cotizaciones.yview)
        tree_cotizaciones.configure(yscrollcommand=scrollbar.set)
        
        tree_cotizaciones.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        def cargar_cotizaciones(termino="", fecha_desde="", fecha_hasta=""):
            for item in tree_cotizaciones.get_children():
                tree_cotizaciones.delete(item)
            
            conn = sqlite3.connect("karnil.db")
            c = conn.cursor()
            
            query = """SELECT numero, fecha, cliente_nombre, cliente_documento, 
                              telefono, subtotal, igv, total, estado 
                       FROM cotizaciones WHERE 1=1"""
            params = []
            
            if termino:
                query += " AND (numero LIKE ? OR cliente_nombre LIKE ? OR cliente_documento LIKE ?)"
                params.extend([f'%{termino}%', f'%{termino}%', f'%{termino}%'])
            
            if fecha_desde:
                query += " AND DATE(fecha) >= ?"
                params.append(fecha_desde)
            
            if fecha_hasta:
                query += " AND DATE(fecha) <= ?"
                params.append(fecha_hasta)
            
            query += " ORDER BY fecha DESC"
            
            c.execute(query, params)
            cotizaciones = c.fetchall()
            conn.close()
            
            for cotizacion in cotizaciones:
                try:
                    fecha_obj = datetime.strptime(cotizacion[1], "%Y-%m-%d %H:%M:%S")
                    fecha_formateada = fecha_obj.strftime("%d/%m/%Y %H:%M")
                except:
                    fecha_formateada = cotizacion[1]
                
                estado = cotizacion[8]
                estado_text = estado
                
                tree_cotizaciones.insert("", "end", values=(
                    cotizacion[0],
                    fecha_formateada,
                    cotizacion[2],
                    cotizacion[3],
                    cotizacion[4],
                    f"S/{cotizacion[5]:.2f}",
                    f"S/{cotizacion[6]:.2f}",
                    f"S/{cotizacion[7]:.2f}",
                    estado_text
                ))
        
        def ver_detalles():
            seleccion = tree_cotizaciones.selection()
            if not seleccion:
                messagebox.showinfo("Detalles", "Seleccione una cotización para ver detalles")
                return
            
            item = tree_cotizaciones.item(seleccion[0])
            numero_cotizacion = item['values'][0]
            
            ventana_detalles = tk.Toplevel(ventana_historial)
            ventana_detalles.title(f"Detalles Cotización: {numero_cotizacion}")
            ventana_detalles.geometry("900x600")
            ventana_detalles.configure(bg="white")
            
            tk.Label(ventana_detalles, text=f"DETALLES COTIZACIÓN: {numero_cotizacion}", 
                    font=("Arial", 14, "bold"), bg="white", fg=self.color_verde_oscuro).pack(pady=10)
            
            conn = sqlite3.connect("karnil.db")
            c = conn.cursor()
            
            c.execute("""SELECT fecha, cliente_nombre, cliente_documento, cliente_tipo,
                                telefono, email, direccion, subtotal, igv, total, con_igv, estado
                         FROM cotizaciones WHERE numero = ?""", (numero_cotizacion,))
            cotizacion = c.fetchone()
            
            info_frame = tk.Frame(ventana_detalles, bg="white", padx=30, pady=10)
            info_frame.pack(fill=tk.X)
            
            if cotizacion:
                try:
                    fecha_obj = datetime.strptime(cotizacion[0], "%Y-%m-%d %H:%M:%S")
                    fecha_formateada = fecha_obj.strftime("%d/%m/%Y %H:%M:%S")
                except:
                    fecha_formateada = cotizacion[0]
                
                info_text = f"""
                Fecha: {fecha_formateada}
                Cliente: {cotizacion[1]}
                Documento: {cotizacion[2]} ({cotizacion[3]})
                Teléfono: {cotizacion[4]}
                Email: {cotizacion[5]}
                Dirección: {cotizacion[6]}
                Estado: {cotizacion[11]}
                """
                
                tk.Label(info_frame, text=info_text, bg="white", font=("Arial", 10),
                        justify=tk.LEFT).pack(anchor='w')
            
            c.execute("""SELECT producto_nombre, talla, cantidad, precio_unitario, color, material
                         FROM cotizacion_detalles 
                         WHERE cotizacion_id = (SELECT id FROM cotizaciones WHERE numero = ?)
                         ORDER BY id""", (numero_cotizacion,))
            
            productos = c.fetchall()
            conn.close()
            
            tabla_frame = tk.Frame(ventana_detalles, bg="white", padx=20, pady=10)
            tabla_frame.pack(fill=tk.BOTH, expand=True)
            
            columns = ("Producto", "Talla", "Cant", "Color", "Material", "Precio S/", "Subtotal S/")
            tree_detalles = ttk.Treeview(tabla_frame, columns=columns, show="headings", height=8)
            
            tree_detalles.heading("Producto", text="Producto")
            tree_detalles.heading("Talla", text="Talla")
            tree_detalles.heading("Cant", text="Cant")
            tree_detalles.heading("Color", text="Color")
            tree_detalles.heading("Material", text="Material")
            tree_detalles.heading("Precio S/", text="Precio S/")
            tree_detalles.heading("Subtotal S/", text="Subtotal S/")
            
            tree_detalles.column("Producto", width=200)
            tree_detalles.column("Talla", width=60, anchor='center')
            tree_detalles.column("Cant", width=50, anchor='center')
            tree_detalles.column("Color", width=70, anchor='center')
            tree_detalles.column("Material", width=100, anchor='center')
            tree_detalles.column("Precio S/", width=80, anchor='e')
            tree_detalles.column("Subtotal S/", width=90, anchor='e')
            
            scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=tree_detalles.yview)
            tree_detalles.configure(yscrollcommand=scrollbar.set)
            
            tree_detalles.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            for producto in productos:
                subtotal = producto[2] * producto[3]
                tree_detalles.insert("", "end", values=(
                    producto[0],
                    producto[1],
                    producto[2],
                    producto[4],
                    producto[5],
                    f"{producto[3]:.2f}",
                    f"{subtotal:.2f}"
                ))
            
            if cotizacion:
                totales_frame = tk.Frame(ventana_detalles, bg="white", padx=30, pady=10)
                totales_frame.pack(fill=tk.X)
                
                tipo_igv = "CON IGV" if cotizacion[10] == 1 else "SIN IGV"
                totales_text = f"""
                Subtotal: S/{cotizacion[7]:.2f}
                IGV: S/{cotizacion[8]:.2f}
                TOTAL: S/{cotizacion[9]:.2f}
                Tipo: {tipo_igv}
                """
                
                tk.Label(totales_frame, text=totales_text, bg="white", font=("Arial", 11, "bold"),
                        justify=tk.LEFT).pack(anchor='w')
        
        def eliminar_cotizacion():
            seleccion = tree_cotizaciones.selection()
            if not seleccion:
                messagebox.showinfo("Eliminar", "Seleccione una cotización para eliminar")
                return
            
            item = tree_cotizaciones.item(seleccion[0])
            numero_cotizacion = item['values'][0]
            
            if messagebox.askyesno("Confirmar Eliminación", 
                                  f"¿Está seguro de eliminar la cotización {numero_cotizacion}?\n\nEsta acción no se puede deshacer."):
                try:
                    conn = sqlite3.connect("karnil.db")
                    c = conn.cursor()
                    
                    c.execute("DELETE FROM cotizacion_detalles WHERE cotizacion_id = (SELECT id FROM cotizaciones WHERE numero = ?)", (numero_cotizacion,))
                    c.execute("DELETE FROM cotizaciones WHERE numero = ?", (numero_cotizacion,))
                    
                    conn.commit()
                    conn.close()
                    
                    messagebox.showinfo("Éxito", f"Cotización {numero_cotizacion} eliminada correctamente")
                    cargar_cotizaciones()
                    
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo eliminar la cotización: {str(e)}")
        
        botones_frame = tk.Frame(ventana_historial, bg="white", pady=10)
        botones_frame.pack(fill=tk.X)
        
        tk.Button(botones_frame, text="👁️ Ver Detalles", bg="#3498DB", fg="white",
                 command=ver_detalles).pack(side=tk.LEFT, padx=20)
        
        tk.Button(botones_frame, text="🗑️ Eliminar Seleccionada", bg=self.color_rojo, fg="white",
                 command=eliminar_cotizacion).pack(side=tk.LEFT, padx=20)
        
        tk.Button(botones_frame, text="🔄 Actualizar", bg="#9B59B6", fg="white",
                 command=lambda: cargar_cotizaciones()).pack(side=tk.LEFT, padx=20)
        
        tk.Button(botones_frame, text="❌ Cerrar", bg="#7F8C8D", fg="white",
                 command=ventana_historial.destroy).pack(side=tk.RIGHT, padx=20)
        
        cargar_cotizaciones()
    
    def nueva_cotizacion(self):
        """Crear nueva cotización"""
        if messagebox.askyesno("Nueva Cotización", "¿Crear nueva cotización?\nSe limpiarán todos los datos."):
            for key, widget in self.entradas_cliente.items():
                if isinstance(widget, tk.Entry):
                    widget.delete(0, tk.END)
                elif isinstance(widget, ttk.Combobox):
                    widget.set(widget['values'][0])
            
            self.entry_nombre_producto.delete(0, tk.END)
            self.entry_material.delete(0, tk.END)
            self.entry_precio_base.delete(0, tk.END)
            self.entry_precio_mayor.delete(0, tk.END)
            
            self.tallas_seleccionadas = []
            self.actualizar_etiqueta_tallas()
            
            self.productos_cotizacion = []
            for item in self.tree_productos.get_children():
                self.tree_productos.delete(item)
            
            self.con_igv.set(True)
            self.check_igv.select()
            self.calcular_totales()
            self.entradas_cliente['nombre_completo'].focus()
    
    def guardar_cotizacion(self):
        """Guardar cotización en archivo de texto y en base de datos"""
        nombre = self.entradas_cliente['nombre_completo'].get().strip()
        documento = self.entradas_cliente['n_documento'].get().strip()
        
        if not nombre:
            messagebox.showerror("Error", "Ingrese el nombre del cliente")
            return
        
        if not documento:
            messagebox.showerror("Error", "Ingrese el número de documento")
            return
        
        if not self.productos_cotizacion:
            messagebox.showerror("Error", "Agregue al menos un producto")
            return
        
        subtotal = sum(p['subtotal'] for p in self.productos_cotizacion)
        con_igv = self.con_igv.get()
        
        if con_igv:
            igv = subtotal * 0.18
            total = subtotal + igv
        else:
            igv = 0
            total = subtotal
        
        fecha = datetime.now()
        numero_base = f"COT-{fecha.strftime('%Y%m%d')}"
        
        try:
            nombre_archivo = f"cotizacion_{numero_base}_{nombre.replace(' ', '_')}.txt"
            
            contenido = []
            contenido.append("=" * 80)
            contenido.append("KARNIL COLLECTION - COTIZACIÓN OFICIAL")
            contenido.append("=" * 80)
            contenido.append(f"\nFECHA: {fecha.strftime('%d/%m/%Y %H:%M')}")
            contenido.append(f"VENDEDOR: KARNIL COLLECTION")
            contenido.append(f"CLIENTE: {nombre}")
            contenido.append(f"DOCUMENTO: {self.entradas_cliente['tipo_documento'].get()} {documento}")
            contenido.append(f"TELÉFONO: {self.entradas_cliente['teléfono'].get()}")
            contenido.append(f"EMAIL: {self.entradas_cliente['email'].get()}")
            contenido.append(f"DIRECCIÓN: {self.entradas_cliente['dirección'].get()}")
            contenido.append("-" * 80)
            
            contenido.append("\nDETALLE DE PRODUCTOS:")
            contenido.append("-" * 80)
            contenido.append(f"{'No.':<4} {'PRODUCTO':<25} {'TALLA':<6} {'CANT':<5} {'COLOR':<8} {'MATERIAL':<15} {'PRECIO':<10} {'SUBTOTAL':<10}")
            contenido.append("-" * 80)
            
            for i, producto in enumerate(self.productos_cotizacion, 1):
                contenido.append(
                    f"{i:<4} "
                    f"{producto['nombre'][:24]:<25} "
                    f"{producto['talla']:<6} "
                    f"{producto['cantidad']:<5} "
                    f"{producto['color'][:7]:<8} "
                    f"{(producto['material'][:14] if producto['material'] else ''):<15} "
                    f"S/{producto['precio']:<9.2f} "
                    f"S/{producto['subtotal']:<9.2f}"
                )
            
            contenido.append("-" * 80)
            
            contenido.append("\nRESUMEN FINANCIERO:")
            contenido.append("-" * 80)
            contenido.append(f"Subtotal: S/{subtotal:.2f}")
            
            if con_igv:
                contenido.append(f"IGV (18%): S/{igv:.2f}")
                contenido.append(f"TOTAL A PAGAR (con IGV): S/{total:.2f}")
            else:
                contenido.append(f"IGV: NO APLICA")
                contenido.append(f"TOTAL A PAGAR (sin IGV): S/{total:.2f}")
            
            contenido.append("-" * 80)
            
            contenido.append("\nDATOS DE CONTACTO:")
            contenido.append("-" * 80)
            contenido.append(f"DIRECCIÓN: {self.datos_empresa['direccion']}")
            contenido.append(f"CONTACTO:")
            contenido.append(f"  Teléfonos : {self.datos_empresa['telefono1']} / {self.datos_empresa['telefono2']}")
            contenido.append(f"  Email: {self.datos_empresa['email']}")
            contenido.append(f"REDES SOCIALES:")
            contenido.append(f"  Instagram: {self.datos_empresa['instagram']}")
            contenido.append(f"  Facebook: {self.datos_empresa['facebook']}")
            contenido.append("-" * 80)
            
            contenido.append("\nNOTAS:")
            contenido.append("- Esta cotización es válida por 30 días")
            contenido.append("- Precios en Soles Peruanos (S/)")
            contenido.append(f"- Cotización {'CON IGV' if con_igv else 'SIN IGV'}")
            contenido.append("- Forma de pago: Transferencia bancaria o efectivo")
            contenido.append("- Tiempo de entrega: 5-10 días hábiles")
            contenido.append("=" * 80)
            contenido.append("\n¡Gracias por su preferencia!")
            contenido.append("KARNIL COLLECTION - Textiles de Calidad")
            contenido.append("=" * 80)
            
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Documentos de texto", "*.txt"), ("Todos los archivos", "*.*")],
                initialfile=nombre_archivo,
                title="Guardar cotización como archivo de texto"
            )
            
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(contenido))
                
                conn = sqlite3.connect("karnil.db")
                c = conn.cursor()
                
                try:
                    c.execute("SELECT COUNT(*) FROM cotizaciones WHERE numero LIKE ?", (f"{numero_base}%",))
                    conteo = c.fetchone()[0] + 1
                    numero_db = f"{numero_base}-{conteo:04d}"
                    
                    c.execute('''INSERT INTO cotizaciones 
                               (numero, fecha, cliente_nombre, cliente_documento, cliente_tipo,
                                telefono, email, direccion, subtotal, igv, total, con_igv, estado, usuario_id)
                               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                             (
                                 numero_db,
                                 fecha.strftime("%Y-%m-%d %H:%M:%S"),
                                 nombre,
                                 documento,
                                 self.entradas_cliente['tipo_documento'].get(),
                                 self.entradas_cliente['teléfono'].get().strip(),
                                 self.entradas_cliente['email'].get().strip(),
                                 self.entradas_cliente['dirección'].get().strip(),
                                 subtotal,
                                 igv,
                                 total,
                                 1 if con_igv else 0,
                                 'PENDIENTE',
                                 self.usuario['id']
                             ))
                    
                    cotizacion_id = c.lastrowid
                    
                    for producto in self.productos_cotizacion:
                        c.execute('''INSERT INTO cotizacion_detalles 
                                   (cotizacion_id, producto_nombre, talla, cantidad, 
                                    precio_unitario, color, material)
                                   VALUES (?, ?, ?, ?, ?, ?, ?)''',
                                 (
                                     cotizacion_id,
                                     producto['nombre'],
                                     producto['talla'],
                                     producto['cantidad'],
                                     producto['precio'],
                                     producto['color'],
                                     producto['material']
                                 ))
                    
                    conn.commit()
                    
                    tipo_igv = "CON IGV" if con_igv else "SIN IGV"
                    messagebox.showinfo("Éxito", 
                                       f"✅ Cotización guardada exitosamente\n\n"
                                       f"📋 Número: {numero_db}\n"
                                       f"👤 Cliente: {nombre}\n"
                                       f"💰 Total: S/{total:.2f}\n"
                                       f"📊 Tipo: {tipo_igv}\n"
                                       f"💾 Archivo guardado: {os.path.basename(file_path)}\n"
                                       f"📅 Fecha: {fecha.strftime('%d/%m/%Y')}\n"
                                       f"📦 Productos: {len(self.productos_cotizacion)} items")
                    
                    self.nueva_cotizacion()
                    
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo guardar en base de datos: {str(e)}")
                finally:
                    conn.close()
                    
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo: {str(e)}")
    
    def exportar_pdf(self):
        """Exportar cotización a PDF real"""
        nombre = self.entradas_cliente['nombre_completo'].get().strip()
        documento = self.entradas_cliente['n_documento'].get().strip()
        
        if not nombre:
            messagebox.showerror("Error", "Ingrese el nombre del cliente")
            return
        
        if not self.productos_cotizacion:
            messagebox.showerror("Error", "Agregue al menos un producto")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Documentos PDF", "*.pdf"), ("Todos los archivos", "*.*")],
            initialfile=f"cotizacion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        )
        
        if not file_path:
            return
        
        try:
            subtotal = sum(p['subtotal'] for p in self.productos_cotizacion)
            con_igv = self.con_igv.get()
            
            if con_igv:
                igv = subtotal * 0.18
                total = subtotal + igv
                tipo_igv_text = "CON IGV (18%)"
            else:
                igv = 0
                total = subtotal
                tipo_igv_text = "SIN IGV"
            
            # Crear documento PDF
            doc = SimpleDocTemplate(file_path, pagesize=A4)
            elements = []
            styles = getSampleStyleSheet()
            
            # Título
            title_style = styles['Title']
            title_style.alignment = 1  # Centrado
            title = Paragraph("KARNIL COLLECTION - COTIZACIÓN OFICIAL", title_style)
            elements.append(title)
            elements.append(Spacer(1, 20))
            
            # Información general
            info_style = styles['Normal']
            fecha = datetime.now().strftime('%d/%m/%Y %H:%M')
            
            info_text = f"""
            <b>Fecha:</b> {fecha}<br/>
            <b>Vendedor:</b> KARNIL COLLECTION<br/>
            <b>Cliente:</b> {nombre}<br/>
            <b>Documento:</b> {self.entradas_cliente['tipo_documento'].get()} {documento}<br/>
            <b>Teléfono:</b> {self.entradas_cliente['teléfono'].get()}<br/>
            <b>Email:</b> {self.entradas_cliente['email'].get()}<br/>
            <b>Dirección:</b> {self.entradas_cliente['dirección'].get()}<br/>
            <b>Tipo de cotización:</b> {tipo_igv_text}<br/>
            """
            
            info_paragraph = Paragraph(info_text, info_style)
            elements.append(info_paragraph)
            elements.append(Spacer(1, 20))
            
            # Encabezado de tabla de productos
            elements.append(Paragraph("<b>DETALLE DE PRODUCTOS:</b>", info_style))
            elements.append(Spacer(1, 10))
            
            # Datos de la tabla
            table_data = [['No.', 'Producto', 'Talla', 'Cant.', 'Color', 'Material', 'Precio S/', 'Subtotal S/']]
            
            for i, producto in enumerate(self.productos_cotizacion, 1):
                table_data.append([
                    str(i),
                    producto['nombre'][:30],
                    producto['talla'],
                    str(producto['cantidad']),
                    producto['color'][:10],
                    producto['material'][:15] if producto['material'] else "",
                    f"{producto['precio']:.2f}",
                    f"{producto['subtotal']:.2f}"
                ])
            
            # Crear tabla
            table = Table(table_data, colWidths=[30, 150, 40, 40, 50, 80, 60, 70])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#006400')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('ALIGN', (5, 0), (-1, -1), 'RIGHT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
            ]))
            
            elements.append(table)
            elements.append(Spacer(1, 20))
            
            # Resumen financiero
            elements.append(Paragraph("<b>RESUMEN FINANCIERO:</b>", info_style))
            elements.append(Spacer(1, 10))
            
            totales_text = f"""
            <b>Subtotal:</b> S/{subtotal:.2f}<br/>
            """
            
            if con_igv:
                totales_text += f"<b>IGV (18%):</b> S/{igv:.2f}<br/>"
                totales_text += f"<b>TOTAL A PAGAR (con IGV):</b> S/{total:.2f}<br/>"
            else:
                totales_text += f"<b>IGV:</b> NO APLICA<br/>"
                totales_text += f"<b>TOTAL A PAGAR (sin IGV):</b> S/{total:.2f}<br/>"
            
            totales_paragraph = Paragraph(totales_text, info_style)
            elements.append(totales_paragraph)
            elements.append(Spacer(1, 20))
            
            # Datos de contacto de la empresa
            elements.append(Paragraph("<b>DATOS DE CONTACTO:</b>", info_style))
            contacto_text = f"""
            <b>DIRECCIÓN:</b><br/>
            {self.datos_empresa['direccion']}<br/><br/>
            <b>CONTACTO:</b><br/>
            Teléfonos: {self.datos_empresa['telefono1']} / {self.datos_empresa['telefono2']}<br/>
            Email: {self.datos_empresa['email']}<br/><br/>
            <b>REDES SOCIALES:</b><br/>
            Instagram: {self.datos_empresa['instagram']}<br/>
            Facebook: {self.datos_empresa['facebook']}<br/>
            """
            contacto_paragraph = Paragraph(contacto_text, info_style)
            elements.append(contacto_paragraph)
            elements.append(Spacer(1, 20))
            
            # Notas
            elements.append(Paragraph("<b>NOTAS:</b>", info_style))
            notas_text = """
            • Esta cotización es válida por 30 días<br/>
            • Precios en Soles Peruanos (S/)<br/>
            • Forma de pago: Transferencia bancaria o efectivo<br/>
            • Tiempo de entrega: 5-10 días hábiles<br/>
            """
            notas_paragraph = Paragraph(notas_text, info_style)
            elements.append(notas_paragraph)
            elements.append(Spacer(1, 20))
            
            # Pie de página
            footer_text = """
            <b>¡Gracias por su preferencia!</b><br/>
            KARNIL COLLECTION - Textiles de Calidad<br/>
            """
            footer_paragraph = Paragraph(footer_text, info_style)
            elements.append(footer_paragraph)
            
            # Generar PDF
            doc.build(elements)
            
            messagebox.showinfo("Éxito", 
                              f"✅ PDF exportado exitosamente:\n{file_path}\n\n"
                              f"El archivo PDF se ha generado correctamente.")
            
            # Abrir el PDF automáticamente
            try:
                webbrowser.open(file_path)
            except:
                pass
            
        except Exception as e:
            messagebox.showerror("Error", f"❌ No se pudo exportar a PDF: {str(e)}")
    
    def exportar_excel(self):
        """Exportar cotización a CSV (compatible con Excel)"""
        nombre = self.entradas_cliente['nombre_completo'].get().strip()
        documento = self.entradas_cliente['n_documento'].get().strip()
        
        if not nombre:
            messagebox.showerror("Error", "Ingrese el nombre del cliente")
            return
        
        if not self.productos_cotizacion:
            messagebox.showerror("Error", "Agregue al menos un producto")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("Archivos Excel (CSV)", "*.csv"), ("Todos los archivos", "*.*")],
            initialfile=f"cotizacion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )
        
        if not file_path:
            return
        
        try:
            subtotal = sum(p['subtotal'] for p in self.productos_cotizacion)
            con_igv = self.con_igv.get()
            
            if con_igv:
                igv = subtotal * 0.18
                total = subtotal + igv
                tipo_igv_text = "CON IGV"
            else:
                igv = 0
                total = subtotal
                tipo_igv_text = "SIN IGV"
            
            with open(file_path, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f, delimiter=';')
                
                writer.writerow(["KARNIL COLLECTION - COTIZACIÓN"])
                writer.writerow([f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}"])
                writer.writerow([f"Vendedor: KARNIL COLLECTION"])
                writer.writerow([f"Cliente: {nombre}"])
                writer.writerow([f"Documento: {self.entradas_cliente['tipo_documento'].get()} {documento}"])
                writer.writerow([f"Teléfono: {self.entradas_cliente['teléfono'].get()}"])
                writer.writerow([f"Correo: {self.entradas_cliente['email'].get()}"])
                writer.writerow([f"Dirección: {self.entradas_cliente['dirección'].get()}"])
                writer.writerow([f"Tipo de cotización: {tipo_igv_text}"])
                writer.writerow([])
                
                writer.writerow(["No.", "Producto", "Talla", "Cantidad", "Color", "Material", "Precio Unitario (S/)", "Subtotal (S/)"])
                
                for i, producto in enumerate(self.productos_cotizacion, 1):
                    writer.writerow([
                        i,
                        producto['nombre'],
                        producto['talla'],
                        producto['cantidad'],
                        producto['color'],
                        producto['material'] if producto['material'] else "",
                        f"{producto['precio']:.2f}",
                        f"{producto['subtotal']:.2f}"
                    ])
                
                writer.writerow([])
                
                writer.writerow(["RESUMEN FINANCIERO:"])
                writer.writerow(["Subtotal (S/):", f"{subtotal:.2f}"])
                
                if con_igv:
                    writer.writerow(["IGV (18%) (S/):", f"{igv:.2f}"])
                    writer.writerow(["TOTAL CON IGV (S/):", f"{total:.2f}"])
                else:
                    writer.writerow(["IGV:", "NO APLICA"])
                    writer.writerow(["TOTAL SIN IGV (S/):", f"{total:.2f}"])
                
                writer.writerow([])
                writer.writerow(["DATOS DE CONTACTO:"])
                writer.writerow(["DIRECCIÓN:", self.datos_empresa['direccion']])
                writer.writerow(["CONTACTO:"])
                writer.writerow(["Teléfonos:", f"{self.datos_empresa['telefono1']} / {self.datos_empresa['telefono2']}"])
                writer.writerow(["Email:", self.datos_empresa['email']])
                writer.writerow(["REDES SOCIALES:"])
                writer.writerow(["Instagram:", self.datos_empresa['instagram']])
                writer.writerow(["Facebook:", self.datos_empresa['facebook']])
                writer.writerow([])
                writer.writerow(["NOTAS:"])
                writer.writerow(["Cotización válida por 30 días"])
                writer.writerow(["Precios en Soles Peruanos (S/)"])
                writer.writerow([f"Tipo de cotización: {tipo_igv_text}"])
                writer.writerow(["Forma de pago: Transferencia bancaria o efectivo"])
                writer.writerow(["Tiempo de entrega: 5-10 días hábiles"])
                writer.writerow(["Gracias por su preferencia - KARNIL COLLECTION"])
            
            messagebox.showinfo("Éxito", 
                              f"✅ Archivo Excel exportado exitosamente:\n{file_path}\n\n"
                              f"📊 Este archivo se abrirá correctamente en Excel.")
            
        except Exception as e:
            messagebox.showerror("Error", f"❌ No se pudo exportar: {str(e)}")

def main():
    root = tk.Tk()
    app = SistemaLogin(root)
    root.mainloop()

if __name__ == "__main__":
    main()