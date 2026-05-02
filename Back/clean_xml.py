import re
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

origen = os.path.join(BASE_DIR, "model", "red_bayesiana.xml")
destino = os.path.join(BASE_DIR, "model", "red_bayesiana_clean.xml")

def limpiar_xml(origen, destino):
    with open(origen, "r", encoding="utf-8", errors="ignore") as f:
        contenido = f.read()

    # quitar &apos;
    contenido = contenido.replace("&apos;", "")

    # quitar comillas simples
    contenido = re.sub(r"'([^']+)'", r"\1", contenido)

    # arreglar caracteres raros
    contenido = contenido.replace(" ", " ")  # espacio invisible
    contenido = contenido.replace("ó", "o")
    contenido = contenido.replace("í", "i")
    contenido = contenido.replace("é", "e")
    contenido = contenido.replace("á", "a")
    contenido = contenido.replace("ú", "u")
    contenido = contenido.replace("ñ", "n")

    # correcciones clave
    contenido = contenido.replace("¿Tiene Emprendimiento?", "Tiene Emprendimiento")

    with open(destino, "w", encoding="utf-8") as f:
        f.write(contenido)

    print("✅ XML LIMPIO GENERADO EN:", destino)


limpiar_xml(origen, destino)