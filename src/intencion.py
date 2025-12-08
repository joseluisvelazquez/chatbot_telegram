import re
from src.sentimiento import predecir_sentimiento
from src.denuncias import predecir_denuncia

# Umbrales para validar detección por modelo ML
CATEGORIAS_DENUNCIA = ["accidente", "bloqueo", "trafico pesado", "agresion"]
SENTIMIENTOS_VALIDOS = ["positivo", "negativo"]



def detectar_intencion(texto: str) -> str:
    t = texto.lower().strip()
    # ====================================================
    # 1. INTENCIÓN: DENUNCIAS Viales / Problemas
    # ====================================================
    patrones_denuncias = [
        r"\baccidente\b",
        r"\bchoque\b",
        r"\bvolcadur[ao]\b",
        r"\bimpact[oó]\b",
        r"\bsemaforo\b",
        r"\bsemáforo\b",
        r"\bapagado\b",
        r"\bno sirve\b",
        r"\bdescompuesto\b",
        r"\bfallando\b",
        r"\bbache\b",
        r"\bagujero\b",
        r"\bzanja\b",
        r"\bbloqueo\b",
        r"\bbloqueada\b",
        r"\bbloqueado\b",
        r"\bmanifestaci[oó]n\b",
        r"\bprotesta\b",
        r"\btrafico\b",
        r"\btr[aá]nsito\b",
        r"\bsaturado\b",
        r"\bmuy lento\b",
        r"\bfuga\b",
        r"\bhumo\b",
        r"\bderrumb[e]\b",
        r"\bposte ca[ií]do\b",
        r"\binundaci[oó]n\b",
        r"\bchocar[oa]n\b",
        r"\bchocaron\b",
        r"\bse chocaron\b",
        r"\bse estrellaron\b",
        r"\bcolisi[oó]n\b",
        r"\bcola de veh[ií]culos\b",
    ]
    for p in patrones_denuncias:
        if re.search(p, t):
            return "denuncia"
    # ====================================================
    # 2. INTENCIÓN: PREGUNTAS DE RUTA / TRANSPORTE
    # ====================================================
    patrones_ruta = [
        r"\bruta\b",
        r"\brutas\b",
        r"\bqué ruta\b",
        r"\bcual ruta\b",
        r"\bpasa por\b",
        r"\bllega a\b",
        r"\bcómo llego\b",
        r"\btransporte\b",
        r"\bcam[ií]on\b",
        r"\bautob[uú]s\b",
        r"\bparada\b",
        r"\bhorario\b",
        r"\bpuente\b",
        r"\bmercado\b",
        r"\bbanth[ií]\b",
        r"\bcomo llego\b",
        r"\bcentro\b", 
        r"\bpaseo central\b",
        r"\bpuente de la historia\b", 
        r"\bpuente\b",
        r"\bhorario\b",
    ]
    for p in patrones_ruta:
        if re.search(p, t):
            return "ruta"
        
    mapa_zonas = {
        "banthí": ["banthi", "rancho banthi", "granjas banthí"],
        "centro": ["mercado", "centro", "5 de mayo", "zona centro","mercado juárez"],
        "las águilas": ["águilas", "las aguilas", "aguilas"],
        "la floresta": ["floresta", "la floresta"],
        "paseo central": ["central", "paseo central", "avenida central","av central"],
        "av. universidad": ["universidad", "aurrera universidad","av universidad", "avenida universidad"],
        "puente de la historia": ["puente", "puente historia","el puente"],
        # para expandir…
    }

    for zona, variantes in mapa_zonas.items():
        for v in variantes:
            if v in t:
                return "ruta"
        
    # ====================================================
    # 3. INTENCIÓN: SENTIMIENTO
    # ====================================================
    patrones_sentimiento_positivo = [
        r"\bfeliz\b",
        r"\bcontent[oa]\b",
        r"\balegre\b",
        r"\bme encanta\b"
        r"😄|😁|😀|🙂|🥳",
    ]
    for p in patrones_sentimiento_positivo:
        if re.search(p, t):
            return "sentimiento"

    patrones_sentimiento_negativo = [
        r"\bestoy\b(?!.*feliz)",  # Estoy... PERO si dice feliz, no es negativo
        r"\bme siento\b(?!.*feliz)",
        r"\bfrustrad[o|a]\b",
        r"\benharto\b",
        r"\bharto\b",
        r"\bmolesto\b",
        r"\btriste\b",
        r"\bme enoja\b",
        r"\bodio\b",
        r"\bodia\b",
        r"😠|😡|😣|😖|😞",
    ]
    for p in patrones_sentimiento_negativo:
        if re.search(p, t):
            return "sentimiento"

    return "general"
