from src.intencion import detectar_intencion
from src.sentimiento import predecir_sentimiento
from src.denuncias import predecir_denuncia
from src.utils import cargar_respuestas_rutas


class Chatbot:

    def __init__(self):
        # Cargar base de datos de rutas
        self.rutas = cargar_respuestas_rutas()

    # ======================================================
    #   PROCESAR MENSAJE PRINCIPAL
    # ======================================================
    def procesar(self, texto: str):
        intencion = detectar_intencion(texto)

        # --- Preguntas sobre rutas ---
        if intencion == "ruta":
            return self.responder_rutas(texto)

        # --- Denuncia clasificada ---
        elif intencion == "denuncia":
            categoria = predecir_denuncia(texto)
            return self.respuesta_denuncia(categoria)

        # --- Análisis de sentimiento ---
        elif intencion == "sentimiento":
            sentimiento = predecir_sentimiento(texto)
            return self.respuesta_sentimiento(sentimiento)

        # --- Conversación general ---
        else:
            return (
                "Estoy aquí para ayudarte 😊\n"
                "• Pregúntame rutas 🚍\n"
                "• Reporta problemas viales 🚧\n"
                "• O puedo analizar tu sentimiento 😄😞\n"
            )

    # ======================================================
    #   RESPUESTA DE RUTAS
    # ======================================================
    def responder_rutas(self, texto):
        texto = texto.lower()

        for zona, respuesta in self.rutas.items():
            if zona in texto:
                return f"""
🚍 *Información sobre la zona {zona.title()}*  
{respuesta}

¿Quieres que te muestre horarios, paradas o rutas alternativas?
""".strip()

        return "Lo siento, aún no tengo información sobre esa zona 🗺️. ¿Puedes darme un punto de referencia?"

    # ======================================================
    #   RESPUESTA DE DENUNCIAS
    # ======================================================
    def respuesta_denuncia(self, categoria):

        mensajes = {
            "accidente": "Gracias por avisar 🙏. Registré tu reporte como *accidente*. Espero que todos estén bien.",
            "agresión": "Lamento escuchar eso 😟. Marcado como *agresión vial*. Esto es importante para seguridad.",
            "bache": "Listo, lo registré como *bache*. Estos problemas afectan mucho la circulación.",
            "bloqueo": "Gracias por avisar. Clasifiqué el reporte como *bloqueo vial*. Esto suele generar retrasos.",
            "semaforo": "Anotado: *semáforo descompuesto*. Esto puede causar confusión en la vía.",
            "trafico": "Entiendo… Se clasificó como *tráfico pesado*. Gracias por tu reporte.",
        }

        return mensajes.get(categoria, f"Tu reporte fue clasificado como: {categoria}.")

    # ======================================================
    #   RESPUESTA DE SENTIMIENTO
    # ======================================================
    def respuesta_sentimiento(self, sentimiento):

        if sentimiento == "positivo":
            return "¡Qué buena vibra! 😊 Me alegra leer eso."
        elif sentimiento == "negativo":
            return "Lamento que te sientas así 😞. Si puedo ayudarte con algo, aquí estoy."
        else:
            return "Recibo tu mensaje. Si quieres, puedo ayudarte con rutas o reportes de tránsito."
