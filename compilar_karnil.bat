@echo off
chcp 65001 > nul
cls
echo.
echo ╔══════════════════════════════════════════════╗
echo ║       COMPILADOR KARNIL COLLECTION v2.0      ║
echo ║        Archivo principal: karnil_collection.py ║
echo ║           Icono: KARNIL.png                  ║
echo ╚══════════════════════════════════════════════╝
echo.

REM ===== CONFIGURACIÓN =====
set "MAIN_FILE=karnil_collection.py"
set "ICON_PNG=KARNIL.png"
set "ICON_ICO=icon.ico"
set "DB_FILE=karnil.db"
set "EXE_NAME=KarnilCollection"
set "OUTPUT_DIR=dist"

echo 📍 Directorio actual: %CD%
echo 📁 Archivo principal: %MAIN_FILE%
echo 🎨 Icono fuente: %ICON_PNG%
echo 📊 Base de datos: %DB_FILE%
echo.

REM ===== VERIFICAR ARCHIVOS =====
echo 🔍 Verificando archivos requeridos...
echo.

if not exist "%MAIN_FILE%" (
    echo ❌ ERROR: No se encuentra "%MAIN_FILE%"
    echo    Verifica que el archivo esté en esta carpeta
    echo.
    pause
    exit /b 1
)
echo ✅ %MAIN_FILE% encontrado

if not exist "%ICON_PNG%" (
    echo ⚠️  ADVERTENCIA: No se encuentra "%ICON_PNG%"
    echo    Buscando alternativas...
    
    dir *.png /b
    if errorlevel 1 (
        echo ❌ No se encontraron archivos PNG
        echo    Se usará icono por defecto de PyInstaller
        set "USE_ICON="
    ) else (
        echo    Se usará el primer PNG encontrado
        set "USE_ICON=--icon=icon.ico"
    )
) else (
    echo ✅ %ICON_PNG% encontrado
    set "USE_ICON=--icon=icon.ico"
)

if not exist "%DB_FILE%" (
    echo ⚠️  ADVERTENCIA: No se encuentra "%DB_FILE%"
    echo    Creando base de datos básica...
    
    python -c "
import sqlite3
import hashlib
import json
from datetime import datetime

print('Creando base de datos karnil.db...')
conn = sqlite3.connect('karnil.db')
c = conn.cursor()

# Tablas (las mismas que en tu código)
c.execute('''CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            nombre TEXT,
            rol TEXT DEFAULT 'vendedor')''')

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

# Usuarios por defecto
usuarios = [
    ('ashu', hashlib.sha256('ashu123'.encode()).hexdigest(), 'Ashu Salazar', 'admin'),
    ('balu', hashlib.sha256('balu123'.encode()).hexdigest(), 'Balu Salazar', 'vendedor'),
    ('sonia', hashlib.sha256('sonia123'.encode()).hexdigest(), 'Sonia Rimache', 'vendedor')
]

for user in usuarios:
    try:
        c.execute('INSERT OR IGNORE INTO usuarios VALUES (NULL,?,?,?,?)', user)
    except:
        pass

# Productos de ejemplo
productos = [
    ('CAM-001', 'Camisa Formal Hombre', 45.00, 40.00, 
     '{\"S\": 10, \"M\": 15, \"L\": 20, \"XL\": 8}', 
     '{\"S\": 45.00, \"M\": 45.00, \"L\": 45.00, \"XL\": 45.00}',
     '{\"S\": [\"Blanco\", \"Azul\"], \"M\": [\"Blanco\", \"Azul\", \"Negro\"], \"L\": [\"Azul\", \"Negro\"], \"XL\": [\"Blanco\"]}',
     '[\"Blanco\", \"Azul\", \"Negro\"]',
     'Algodón 100%'),
    ('VES-001', 'Vestido Elegante Mujer', 85.00, 75.00, 
     '{\"S\": 5, \"M\": 8, \"L\": 6}', 
     '{\"S\": 85.00, \"M\": 85.00, \"L\": 85.00}',
     '{\"S\": [\"Rojo\", \"Negro\"], \"M\": [\"Rojo\", \"Negro\", \"Blanco\"], \"L\": [\"Negro\", \"Blanco\"]}',
     '[\"Rojo\", \"Negro\", \"Blanco\"]',
     'Seda Natural')
]

for prod in productos:
    try:
        c.execute('INSERT OR IGNORE INTO productos VALUES (NULL,?,?,?,?,?,?,?,?,?,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)', prod)
    except:
        pass

conn.commit()
print(f'✅ Base de datos creada con:')
print(f'   - {len(usuarios)} usuarios')
print(f'   - {len(productos)} productos')
conn.close()
"
    if exist "%DB_FILE%" (
        echo ✅ %DB_FILE% creada exitosamente
    ) else (
        echo ❌ Error al crear la base de datos
    )
) else (
    echo ✅ %DB_FILE% encontrada
)

REM ===== CONVERTIR ICONO =====
echo.
echo 🎨 Procesando icono...
if exist "%ICON_PNG%" (
    if not exist "%ICON_ICO%" (
        echo 🔄 Convirtiendo %ICON_PNG% a %ICON_ICO%...
        python convertir_icono.py
        
        if not exist "%ICON_ICO%" (
            echo ❌ Error al crear icon.ico
            echo    Continuando sin icono personalizado...
            set "USE_ICON="
        )
    ) else (
        echo ✅ %ICON_ICO% ya existe
    )
)

REM ===== LIMPIAR COMPILACIONES ANTERIORES =====
echo.
echo 🧹 Limpiando archivos anteriores...
for %%d in (build dist __pycache__) do (
    if exist "%%d" (
        echo    Eliminando %%d...
        rmdir /s /q "%%d" 2>nul
    )
)
for %%f in (*.spec *.log) do (
    if exist "%%f" (
        echo    Eliminando %%f...
        del "%%f" 2>nul
    )
)

REM ===== COMPILAR =====
echo.
echo 🚀 Iniciando compilación de %MAIN_FILE%...
echo ⏳ Por favor espera, esto puede tomar 2-5 minutos...
echo 📝 Se generarán archivos en las carpetas 'build' y 'dist'
echo.

set "PYINSTALLER_CMD=pyinstaller --onefile --windowed --name="%EXE_NAME%" --add-data "%DB_FILE%;." --hidden-import=reportlab --hidden-import=reportlab.lib --hidden-import=reportlab.pdfbase.ttfonts --hidden-import=PIL --hidden-import=PIL._imagingtk --hidden-import=PIL._imagingft --hidden-import=sqlite3 --hidden-import=tkinter --hidden-import=hashlib --hidden-import=json --hidden-import=webbrowser --clean --noconfirm"

if defined USE_ICON (
    echo 📌 Usando icono personalizado: %ICON_ICO%
    set "PYINSTALLER_CMD=%PYINSTALLER_CMD% --icon=%ICON_ICO%"
) else (
    echo 📌 Usando icono por defecto de PyInstaller
)

echo.
echo 🔧 Comando ejecutado:
echo    %PYINSTALLER_CMD% %MAIN_FILE%
echo.

%PYINSTALLER_CMD% %MAIN_FILE%

REM ===== VERIFICAR RESULTADO =====
echo.
if exist "%OUTPUT_DIR%\%EXE_NAME%.exe" (
    echo 🎉 ¡COMPILACIÓN EXITOSA!
    echo.
    
    REM Obtener tamaño del ejecutable
    for /f "tokens=3" %%a in ('dir /-c "%OUTPUT_DIR%\%EXE_NAME%.exe" ^| findstr "%EXE_NAME%.exe"') do set "EXE_SIZE=%%a"
    
    echo 📍 Ruta del ejecutable: %CD%\%OUTPUT_DIR%\%EXE_NAME%.exe
    echo 📊 Tamaño del archivo: %EXE_SIZE% bytes
    
    echo.
    echo 📋 INSTRUCCIONES PARA DISTRIBUIR:
    echo    1. Copia la carpeta COMPLETA "%OUTPUT_DIR%"
    echo    2. El usuario solo necesita ejecutar "%EXE_NAME%.exe"
    echo    3. NO necesita instalar Python ni dependencias
    
    echo.
    echo 🔐 DATOS DE ACCESO POR DEFECTO:
    echo    Usuario: ashu     Contraseña: ashu123   (Administrador)
    echo    Usuario: balu     Contraseña: balu123   (Vendedor)
    echo    Usuario: sonia    Contraseña: sonia123  (Vendedor)
    
    echo.
    echo 🖱️  ¿Deseas probar la aplicación ahora? (S/N)
    choice /c SN /n /m "Selecciona opción: "
    if errorlevel 2 (
        echo.
        echo ✅ Compilación completada. El ejecutable está listo en:
        echo    📂 %CD%\%OUTPUT_DIR%\
    ) else (
        echo.
        echo 🔧 Ejecutando %EXE_NAME%.exe...
        echo    (Cierra la aplicación para continuar)
        echo.
        start "" "%OUTPUT_DIR%\%EXE_NAME%.exe"
    )
) else (
    echo ❌ ERROR: No se pudo crear el ejecutable
    echo.
    echo 🔍 POSIBLES SOLUCIONES:
    echo    1. Verifica que Python esté en el PATH
    echo    2. Instala dependencias: pip install pillow reportlab
    echo    3. Ejecuta este script como Administrador
    echo    4. Verifica que %MAIN_FILE% no tenga errores de sintaxis
    echo.
    echo 📝 Para ver errores detallados, ejecuta:
    echo    pyinstaller %MAIN_FILE%
)

echo.
echo ═══════════════════════════════════════════
pause