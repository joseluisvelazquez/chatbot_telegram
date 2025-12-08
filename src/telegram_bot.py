from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv
from src.chatbot import Chatbot
import os

load_dotenv()

bot_ia = Chatbot()
TOKEN = os.getenv("BOT_TOKEN")

def start(update, context):
    update.message.reply_text(
        "👋 ¡Hola! Soy tu asistente de movilidad de San Juan del Río 🚍\n"
        "Pregúntame sobre transporte, tráfico o cómo te sientes 😊"
    )

def manejar_mensaje(update, context):
    texto = update.message.text
    respuesta = bot_ia.procesar(texto)
    update.message.reply_text(respuesta)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, manejar_mensaje))

    print("🤖 Bot iniciado en Telegram…")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
