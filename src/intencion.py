import re

# -------------------------------------------
# DETECTOR DE INTENCIONES (versión básica)
# -------------------------------------------

def detectar_intencion(texto: str) -> str:
    texto = texto.lower().strip()

    # 1. Preguntas sobre rutas
    patrones_rutas = [
        r"\bruta\b",
        r"\brutas\b",
        r"\bqué ruta\b",
        r"\bcual ruta\b",
        r"\bpasa por\b",
        r"\bllega a\b",
        r"\bcómo llego\b",
        r"\btransporte\b",
        r"\bcamión\b",
    ]
    for p in patrones_rutas:
        if re.search(p, texto):
            return "ruta"

    # 2. Denuncias (cosas viales)
    patrones_denuncias = [
        r"\baccidente\b",
        r"\bchoc[óo]\b",
        r"\batiendo\b",
        r"\bagresion\b",
        r"\bpele[ae]\b",
        r"\bbloqueo\b",
        r"\bmanifestacion\b",
        r"\bprotesta\b",
        r"\bsemaforo\b",
        r"\bvolte[oó]\b",
        r"\bderrumb[e]\b",
        r"\btrafico\b",
        r"\bmuy lleno\b",
        r"\bobstruido\b",
    ]
    for p in patrones_denuncias:
        if re.search(p, texto):
            return "denuncia"

    # 3. Sentimiento (genérico)
    patrones_sentimiento = [
        r"\bestoy\b",
        r"\bme siento\b",
        r"\bme enoja\b",
        r"\bme gusta\b",
        r"\bno me gusta\b",
        r"\bodia[o]\b",
        r"\btriste\b",
        r"\bfeliz\b",
        r"\bmolesto\b",
        r"\bfrustrado\b",
    ]
    for p in patrones_sentimiento:
        if re.search(p, texto):
            return "sentimiento"

    # 4. Conversación general
    return "general"
