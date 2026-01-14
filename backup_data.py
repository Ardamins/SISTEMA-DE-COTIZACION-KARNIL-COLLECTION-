# backup_data.py
import sqlite3
import shutil
from datetime import datetime
import os

def backup_database():
    """Crear respaldo de la base de datos"""
    if os.path.exists('karnil.db'):
        fecha = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = f'backup_karnil_{fecha}.db'
        
        # Copiar archivo
        shutil.copy2('karnil.db', backup_file)
        
        print(f"✅ Respaldo creado: {backup_file}")
        print(f"📊 Tamaño: {os.path.getsize(backup_file):,} bytes")
        
        # Mostrar estadísticas
        conn = sqlite3.connect('karnil.db')
        c = conn.cursor()
        
        c.execute("SELECT COUNT(*) FROM usuarios")
        usuarios = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM productos")
        productos = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM cotizaciones")
        cotizaciones = c.fetchone()[0]
        
        conn.close()
        
        print(f"📈 Estadísticas:")
        print(f"   👥 Usuarios: {usuarios}")
        print(f"   📦 Productos: {productos}")
        print(f"   📋 Cotizaciones: {cotizaciones}")
        
    else:
        print("❌ No se encontró karnil.db")

if __name__ == "__main__":
    print("=== RESPALDO KARNIL COLLECTION ===")
    backup_database()
    input("\nPresiona Enter para salir...")