import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score
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

def predecir_sentimiento(texto: str):
    modelo = joblib.load("modelos/modelo_sentimiento.pkl")
    vectorizador = joblib.load("modelos/vectorizador_sentimiento.pkl")


    texto_limpio = limpiar_texto(texto)
    vector = vectorizador.transform([texto_limpio])

    pred = modelo.predict(vector)[0]
    return pred


if __name__ == "__main__":
    entrenar_modelo_sentimiento()
