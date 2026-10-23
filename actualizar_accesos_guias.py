from pathlib import Path
import re
import shutil
import subprocess

BASE = Path(__file__).resolve().parent
LANZADOR = BASE / "abrir_python.sh"
APLICACIONES = Path.home() / ".local/share/applications"
APLICACIONES.mkdir(parents=True, exist_ok=True)


def argumento_exec(ruta):
    return '"' + str(ruta).replace("\\", "\\\\").replace('"', '\\"') + '"'


def crear_acceso(archivo, nombre, destino, comentario):
    comando = (
        "/usr/bin/bash "
        + argumento_exec(LANZADOR)
        + " "
        + argumento_exec(destino)
    )

    contenido = f"""[Desktop Entry]
Version=1.0
Type=Application
Name={nombre}
Comment={comentario}
Exec={comando}
Terminal=true
Icon=utilities-terminal
Categories=Education;Development;
StartupNotify=true
"""

    archivo.write_text(contenido, encoding="utf-8")
    archivo.chmod(0o755)


crear_acceso(
    APLICACIONES / "programacion-ii-python.desktop",
    "Programación II - Python",
    BASE,
    "Abre Python con el entorno virtual activado",
)

guias = [
    carpeta for carpeta in BASE.iterdir()
    if carpeta.is_dir()
    and re.match(r"^gu[ií]a\s*\d+", carpeta.name, re.IGNORECASE)
]

guias.sort(key=lambda p: int(re.search(r"\d+", p.name).group()))

for carpeta in guias:
    numero = re.search(r"\d+", carpeta.name).group()
    crear_acceso(
        APLICACIONES / f"programacion-ii-guia-{numero}.desktop",
        f"Programación II - Guía {numero}",
        carpeta,
        f"Abre {carpeta.name} con el entorno virtual activado",
    )
    print(f"Acceso creado: Programación II - Guía {numero}")

if shutil.which("update-desktop-database"):
    subprocess.run(
        ["update-desktop-database", str(APLICACIONES)],
        check=False,
    )

print("Listo. Los accesos están instalados en el menú de Ubuntu.")
print("Buscá 'Programación II' pulsando la tecla Super.")
