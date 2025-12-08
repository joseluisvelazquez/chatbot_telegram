import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score
from .preprocesamiento import limpiar_texto
import joblib

from .preprocesamiento import limpiar_texto

# -----------------------------------------------------------
# A3 — ENTRENAMIENTO DEL MODELO DE SENTIMIENTO
# -----------------------------------------------------------

def entrenar_modelo_sentimiento(ruta_dataset="data/quejas.csv"):
    # 1. Cargar dataset
    df = pd.read_csv(ruta_dataset)

    # 2. Limpiar textos
    df["texto_limpio"] = df["texto"].apply(limpiar_texto)

    # Variables
    X = df["texto_limpio"]
    y = df["sentimiento"]

    # 3. Dividir en train/test (80/20)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    # 4. Vectorizador TF-IDF
    vectorizador = TfidfVectorizer()
    X_train_tfidf = vectorizador.fit_transform(X_train)
    X_test_tfidf = vectorizador.transform(X_test)

    # 5. Modelo Naive Bayes
    modelo = MultinomialNB()
    modelo.fit(X_train_tfidf, y_train)

    # 6. Evaluación
    predicciones = modelo.predict(X_test_tfidf)

    print("=========== RESULTADOS ===========")
    print("Accuracy:", accuracy_score(y_test, predicciones))
    print("\nReporte completo:\n")
    print(classification_report(y_test, predicciones))

    # 7. Guardar modelo + vectorizador
    joblib.dump(modelo, "modelos/modelo_sentimiento.pkl")
    joblib.dump(vectorizador, "modelos/vectorizador_sentimiento.pkl")

    print("\n✔ Modelo de sentimiento guardado correctamente.")
    print("✔ Ubicación: /models/")


# -----------------------------------------------------------
# A4 — FUNCIÓN DE PREDICCIÓN LISTA PARA EL CHATBOT
# -----------------------------------------------------------

def predecir_sentimiento(texto: str) -> str:
    t = limpiar_texto(texto)

    # 🔹 Prioridad a emociones positivas primero
    positivas = [
        "feliz", "me encanta", "contento", "contenta", "alegre",
        "emocionado", "emocionada", "que bonito"
    ]
    if any(p in t for p in positivas):
        return "positivo"

    negativas = [
        "odio", "estres", "enojo", "molest", "frustrad", "triste",
        "cansado", "cansada", "harto", "harta", "estresado",
        "estresada", "aburrido", "aburrida", "deprimido", "deprimida", "irritado", "irritada",
        "puto  tráfico", "maldito tráfico", "pésimo servicio", "pesimo servicio"
    ]
    if any(n in t for n in negativas):
        return "negativo"

    return "neutro"