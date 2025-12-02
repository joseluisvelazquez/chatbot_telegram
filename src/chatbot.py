from src.intencion import detectar_intencion
from src.sentimiento import predecir_sentimiento
from src.denuncias import predecir_denuncia
from src.utils import cargar_respuestas_rutas


class Chatbot:

    def __init__(self):
        # Cargar base de datos de rutas
        self.rutas = cargar_respuestas_rutas()

    def procesar(self, texto: str):
        """Decide qué acción ejecutar según la intención detectada."""

        intencion = detectar_intencion(texto)

        # --- Preguntas sobre rutas ---
        if intencion == "ruta":
            return self.responder_rutas(texto)

        # --- Denuncia clasificada por modelo ---
        elif intencion == "denuncia":
            categoria = predecir_denuncia(texto)
            return f"Gracias por tu reporte. Se clasificó como: {categoria}"

        # --- Análisis de sentimiento ---
        elif intencion == "sentimiento":
            sentimiento = predecir_sentimiento(texto)
            return f"Sentimiento detectado: {sentimiento}"

        # --- Conversación general ---
        else:
            return "Puedo ayudarte con rutas, quejas de tránsito o analizar tu sentimiento."

    # ------------------------------
    # RESPUESTAS DE RUTAS
    # ------------------------------
    def responder_rutas(self, texto):
        texto = texto.lower()

        for zona, respuesta in self.rutas.items():
            if zona in texto:
                return respuesta

        return "No tengo información sobre esa zona aún."
