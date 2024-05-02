import os
import re
import requests

def sanitizar_nombre_archivo(nombre_archivo):
    # Reemplazar caracteres no válidos con guiones bajos
    nombre_archivo = re.sub(r'[\\/:\*\?"<>\|]', '_', nombre_archivo)
    return nombre_archivo

def descargar_imagen(url_imagen, directorio_destino):
    nombre_archivo = os.path.basename(url_imagen)
    # Sanitizar el nombre del archivo
    nombre_archivo = sanitizar_nombre_archivo(nombre_archivo)
    ruta_archivo = os.path.join(directorio_destino, nombre_archivo)

    try:
        response = requests.get(url_imagen, stream=True)
        if response.status_code == 200:
            with open(ruta_archivo, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            return nombre_archivo, ruta_archivo
        else:
            print(f"Error al descargar la imagen: {response.status_code}")
            return None, None
    except Exception as e:
        print(f"Error al descargar la imagen: {e}")
        return None, None
    
