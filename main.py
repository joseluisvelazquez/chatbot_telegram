from src.chatbot import Chatbot

if __name__ == "__main__":
    bot = Chatbot()

    while True:
        texto = input("\nEscribe tu mensaje: ")

        if texto.lower() in ["salir", "quit", "exit"]:
            print("Adiós 👋")
            break

        respuesta = bot.procesar(texto)
        print(respuesta)
  