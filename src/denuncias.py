import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score
import joblib

from src.preprocesamiento import limpiar_texto

# ENTRENAR MODELO DE DENUNCIAS
def entrenar_modelo_denuncias(ruta="data/denuncias.csv"):
    df = pd.read_csv(ruta)

    df["texto_limpio"] = df["texto"].apply(limpiar_texto)

    X = df["texto_limpio"]
    y = df["tipo"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    vectorizador = TfidfVectorizer()
    X_train_tfidf = vectorizador.fit_transform(X_train)
    X_test_tfidf = vectorizador.transform(X_test)

    modelo = MultinomialNB()
    modelo.fit(X_train_tfidf, y_train)

    pred = modelo.predict(X_test_tfidf)

    print("\n=== RESULTADOS (DENUNCIAS) ===")
    print("Accuracy:", accuracy_score(y_test, pred))
    print("\nReporte completo:\n", classification_report(y_test, pred))

    joblib.dump(modelo, "modelos/modelo_denuncias.pkl")
    joblib.dump(vectorizador, "modelos/vectorizador_denuncias.pkl")

    print("\n✔ Modelo de denuncias guardado.")
    print("✔ Ubicación: /modelos/")


# PREDICCIÓN LISTA PARA EL CHATBOT
def predecir_denuncia(texto: str):
    modelo = joblib.load("modelos/modelo_denuncias.pkl")
    vectorizador = joblib.load("modelos/vectorizador_denuncias.pkl")

    texto_limpio = limpiar_texto(texto)
    vector = vectorizador.transform([texto_limpio])

    categoria = modelo.predict(vector)[0]
    return categoria

if __name__ == "__main__":
    entrenar_modelo_denuncias()
