# convertir_icono.py
from PIL import Image
import os

print("=== CONVERSOR DE ICONO KARNIL COLLECTION ===")
print()

# Listar archivos PNG disponibles
png_files = [f for f in os.listdir() if f.lower().endswith('.png')]
if png_files:
    print("📁 Archivos PNG encontrados:")
    for i, file in enumerate(png_files, 1):
        print(f"   {i}. {file}")
    print()
else:
    print("❌ No se encontraron archivos PNG en la carpeta")
    print("   Coloca KARNIL.png en esta carpeta")
    input("\nPresiona Enter para salir...")
    exit()

# Buscar específicamente KARNIL.png
icon_files = ['KARNIL.png', 'karnil.png', 'icon.png', 'Icon.png']
icon_found = None

for icon_file in icon_files:
    if os.path.exists(icon_file):
        icon_found = icon_file
        break

if not icon_found:
    # Usar el primer PNG encontrado
    icon_found = png_files[0]
    print(f"⚠️  No se encontró KARNIL.png, usando: {icon_found}")
else:
    print(f"✅ Icono encontrado: {icon_found}")

try:
    print(f"\n📷 Abriendo {icon_found}...")
    img = Image.open(icon_found)
    
    # Verificar tamaño
    width, height = img.size
    print(f"   Tamaño: {width}x{height} pixels")
    
    # Convertir a RGB si tiene transparencia
    if img.mode in ('RGBA', 'LA', 'P'):
        print("   Convirtiendo de RGBA a RGB...")
        background = Image.new('RGB', img.size, (255, 255, 255))
        if img.mode == 'P':
            img = img.convert('RGBA')
        background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
        img = background
    
    print("🔄 Creando icon.ico con múltiples resoluciones...")
    
    # Crear icono con diferentes tamaños
    icon_sizes = [(256, 256), (128, 128), (64, 64), 
                  (48, 48), (32, 32), (24, 24), (16, 16)]
    
    img.save('icon.ico', 
             format='ICO', 
             sizes=icon_sizes,
             append_images=[img.resize(size, Image.Resampling.LANCZOS) 
                          for size in icon_sizes[1:]])
    
    print("✅ ¡Icono convertido exitosamente!")
    print(f"📁 Archivo creado: icon.ico")
    print(f"📏 Tamaños incluidos: {', '.join(f'{w}x{h}' for w, h in icon_sizes)}")
    
    # Mostrar vista previa
    print("\n🎨 Vista previa del icono:")
    print("   ┌────────────────────┐")
    print("   │  KARNIL COLLECTION │")
    print("   │     [ICONO]        │")
    print("   └────────────────────┘")
    
except FileNotFoundError:
    print(f"❌ Error: No se pudo abrir {icon_found}")
except Exception as e:
    print(f"❌ Error durante la conversión: {e}")

print("\n" + "="*50)
input("Presiona Enter para continuar...")