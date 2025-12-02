import json

def cargar_respuestas_rutas(ruta="data/rutas_respuestas.json"):
    """Carga las respuestas predefinidas de movilidad desde un JSON."""
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("⚠ No se encontró el archivo rutas_respuestas.json")
        return {}
