from src.intencion import detectar_intencion
from src.sentimiento import predecir_sentimiento
from src.denuncias import predecir_denuncia
from src.utils import cargar_respuestas_rutas
import re

class Chatbot:

    def __init__(self):
        self.rutas = cargar_respuestas_rutas()

    # ======================================================
    #   PROCESAR MENSAJE PRINCIPAL
    # ======================================================
    def procesar(self, texto: str):
        intencion = detectar_intencion(texto.lower())
        texto_l = texto.lower()

            # 👋 SALUDOS
        if texto_l in ["hola", "buenas", "hi", "hello"]:
            return "¡Hola! 👋 ¿Cómo puedo ayudarte hoy? 🚍🙂"

        # ❓ AYUDA / ¿QUÉ PUEDES HACER?
        if "ayuda" in texto_l or "qué puedes hacer" in texto_l \
            or "que haces" in texto_l or "puedes hacer" in texto_l:
                return (
                    "🧠 Puedo ayudarte con:\n"
                    "• Información de rutas de transporte 🚍\n"
                    "• Reportes de tráfico 🚧\n"
                    "• Baches, semáforos apagados, bloqueos 📍\n"
                    "• También puedo escuchar cómo te sientes 😊\n\n"
                    "¿Qué necesitas ahora?"
                )
         # 🚍 Información general de rutas

        if any(frase in texto_l for frase in [
            "info rutas", "información de rutas", "qué rutas hay", 
            "rutas disponibles", "camiones disponibles", "zonas de transporte"
        ]):
            zonas = "\n".join(f"• {z.title()}" for z in self.rutas.keys())
            return (
                "🚍 Actualmente puedo informarte sobre estas zonas:\n\n"
                f"{zonas}\n\n"
                "¿De cuál te gustaría saber más?"
            )

        # ⭐ Si menciona rutas y también frustración → priorizar transporte
        if intencion == "ruta" and any(p in texto_l for p in ["frustrad", "enoja", "molest", "harto"]):
            return "Entiendo que la situación del transporte puede ser incómoda 😣.\n"\
                   "Si me dices el punto exacto de donde estás, puedo ayudarte a encontrar otra opción 🚍."

        # --- Preguntas sobre rutas ---
        if intencion == "ruta":
            return self.responder_rutas(texto)

        # --- Denuncia clasificada ---
        elif intencion == "denuncia":
            categoria = predecir_denuncia(texto)
            return self.respuesta_denuncia(categoria)

        # --- Análisis de sentimiento ---
        elif intencion == "sentimiento":
            sentimiento = predecir_sentimiento(texto.lower())

            if sentimiento == "positivo":
                return "¡Qué buena vibra! 😄 Me alegra leer eso 🌞"

            elif sentimiento == "negativo":
                return ("Lamento que estés pasando por eso 😔.\n"
                        "Si es por el transporte o el tráfico 🚍🚦, dime dónde y te ayudo con opciones.")

            return "Gracias por compartir cómo te sientes 🧡. ¿Quieres que te ayude con transporte o vialidad?"
        
        # --- Conversación general / Small talk ---
        else:
            return (
                "¡Qué buena vibra! 😄\n"
                "Puedo apoyarte con información de rutas 🚍, reportes viales 🚧 "
                "o también puedo analizar cómo te sientes 😊.\n"
                "¿En qué puedo ayudarte?"
            )


    # ======================================================
    #   DETECTAR SENTIMIENTO PRESENTE EN TEXTO
    # ======================================================
    def _menciona_sentimiento(self, texto: str):
        patrones_triste = ["frustrad", "enoja", "molest", "estres", "cansad", "harto"]
        return any(p in texto.lower() for p in patrones_triste)

    # ======================================================
    #   RESPUESTA RUTAS
    # ======================================================

    def responder_rutas(self, texto):
        import unicodedata
        # Normalizamos acentos para mejorar coincidencias
        texto_norm = unicodedata.normalize("NFD", texto.lower()).encode("ascii", "ignore").decode("utf-8")

        # Detectar números de ruta
        import re
        num = re.findall(r"\b\d+\b", texto_norm)
        if num:
            return f"¿En qué parte estás esperando la ruta {num[0]}? 🚏 Para ayudarte mejor, dame un punto de referencia."

        # Buscar zonas desde JSON
        for zona, respuesta in self.rutas.items():
            zona_norm = unicodedata.normalize("NFD", zona.lower()).encode("ascii", "ignore").decode("utf-8")

            if zona_norm in texto_norm:
                return f"""
    📍 *Zona detectada:* **{zona.title()}**

    {respuesta}

    ¿Quieres que también te muestre horarios⏱️, paradas🚌 o rutas alternativas❓
    """.strip()

        return "Aún no tengo información sobre esa zona 🗺️.\n¿Podrías darme una referencia cercana? Como una colonia, plaza o avenida 😊"


    # ======================================================
    #   RESPUESTA RUTAS + EMOCIÓN
    # ======================================================
    def _respuesta_ruta_con_emocion(self, texto):
        return (
            "Entiendo que la situación del transporte puede ser incómoda 😣.\n"
            "Si me dices el punto exacto de donde estás, puedo ayudarte a encontrar otra opción 🚍."
        )

    # ======================================================
    #   RESPUESTA DENUNCIAS
    # ======================================================
    def respuesta_denuncia(self, categoria):
        mensajes = {
            "accidente": "Gracias por avisar 🙏. Registré tu reporte como *accidente*. Espero que todos estén bien.",
            "bloqueo": "Gracias por avisar. Clasifiqué el reporte como *bloqueo vial*. Esto suele generar retrasos.",
            "bache": "Gracias por reportarlo ⚠️. Lo marqué como *bache*, esto puede ser peligroso para vehículos.",
            "semaforo": "Anotado 📝: *semáforo descompuesto o apagado*. Esto puede generar confusión, gracias por avisar.",
            "trafico": "Entiendo… Se clasificó como *tráfico pesado*. Gracias por tu reporte."
        }

        if categoria in mensajes:
            return mensajes[categoria]

        return "Gracias por tu reporte 🚧. Seguiremos al pendiente del tránsito en la zona."


    # ======================================================
    #   RESPUESTA SENTIMIENTO
    # ======================================================
    def respuesta_sentimiento(self, sentimiento):

        if sentimiento == "positivo":
            return "¡Qué buena vibra! 😄 Me alegra que tengas un buen día ✨"

        elif sentimiento == "negativo":
            return (
                "Lamento que estés pasando por eso 😔.\n"
                "Si el problema es con una ruta o en la vía, puedo ayudarte a buscar otra alternativa 🚍.\n"
                "No estás solo 👍"
            )

        return "Gracias por compartir cómo te sientes 😊. ¿Puedo ayudarte con transporte o vialidad?"
