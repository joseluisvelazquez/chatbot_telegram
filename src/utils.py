import json

def cargar_respuestas_rutas():
    with open("data/rutas_sjr.json", "r", encoding="utf-8") as f:
        return json.load(f)
