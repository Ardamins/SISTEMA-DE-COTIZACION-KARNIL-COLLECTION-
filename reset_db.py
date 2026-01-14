import os
import sqlite3

# Borrar la base de datos si existe
if os.path.exists("karnil.db"):
    os.remove("karnil.db")
    print("✅ Base de datos eliminada. Se creará una nueva al ejecutar el programa.")
else:
    print("⚠️  No se encontró la base de datos karnil.db")