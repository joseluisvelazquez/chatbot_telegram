import spacy
import re
import unicodedata

# Carga del modelo en español
nlp = spacy.load("es_core_news_sm")

# Stopwords en español
stopwords_es = nlp.Defaults.stop_words

def limpiar_texto(texto: str) -> str:
    """
    Normaliza, limpia y preprocesa texto para análisis de sentimiento
    y clasificación de denuncias.
    """

    if not isinstance(texto, str):
        return ""

    # 1. Normalizar unicode (eliminar acentos)
    texto = unicodedata.normalize("NFKD", texto).encode("ASCII", "ignore").decode("utf-8", "")

    # 2. Convertir a minúsculas
    texto = texto.lower()

    # 3. Eliminar URLs
    texto = re.sub(r"http\S+|www\.\S+", " ", texto)

    # 4. Eliminar números
    texto = re.sub(r"\d+", " ", texto)

    # 5. Eliminar emojis y caracteres especiales raros
    texto = texto.encode("ascii", "ignore").decode("ascii")

    # 6. Eliminar puntuación
    texto = re.sub(r"[^\w\s]", " ", texto)

    # 7. Procesar con spaCy para tokenizar y lematizar
    doc = nlp(texto)

    tokens_limpios = []

    for token in doc:
        if (
            token.text not in stopwords_es
            and len(token.text) > 2
            and not token.is_space
        ):
            tokens_limpios.append(token.lemma_)

    texto_final = " ".join(tokens_limpios)

    return texto_final


# Prueba rápida (solo para verificar)
if __name__ == "__main__":
    ejemplo = "El tráfico está horrible 😡 en la carretera 57, había un choque!"
    print("Entrada:", ejemplo)
    print("Salida:", limpiar_texto(ejemplo))
