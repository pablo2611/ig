import requests
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import instaloader
import io
import random

# Tu token de API de Telegram
API_TOKEN = '7264857511:AAFYlyYnWrlC5Eojst2_DI1ODrgn7mqnP0A'

# Mensaje personalizado
CUSTOM_MESSAGE = "Gracias por usar nuestro bot @downloadInstagramandmorebot 🤖📸\nÚnete a nuestro canal @Cuentasnew 🌟✨"

# Listas de emojis para seleccionar aleatoriamente
EMOJIS_LIST = [
    '📸✨ Procesando información... 🍿💫',
    '🌟📷 Obteniendo contenido... 🎥🌠',
    '🎉📸 Descargando datos... 🎬🎊',
    '⚡📷 Preparando tus archivos... 🚀✨',
    '💫🎥 Procesando tu solicitud... 🌠🍿'
]

# Función para seleccionar un conjunto de emojis aleatoriamente
def get_random_emojis():
    return random.choice(EMOJIS_LIST)

# Función de inicio /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('¡Hola! Soy tu bot de Telegram 🤖. ¿En qué puedo ayudarte hoy? 🌟')

# Función de ayuda /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Puedes enviarme cualquier mensaje y te responderé. 📩')

# Función que maneja los mensajes de texto y enlaces de Instagram
async def process_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    if "instagram.com" in user_message:
        await update.message.reply_text(get_random_emojis())
        try:
            await download_and_send_instagram_content(update, context, user_message)
        except Exception as e:
            print(f'Error al procesar el enlace: {e}')
    else:
        await update.message.reply_text(get_random_emojis())

async def download_and_send_instagram_content(update: Update, context: ContextTypes.DEFAULT_TYPE, url: str) -> None:
    loader = instaloader.Instaloader()
    post = instaloader.Post.from_shortcode(loader.context, url.split("/")[-2])

    try:
        if post.is_video:
            video_url = post.video_url
            video_content = download_content(video_url)
            await context.bot.send_video(chat_id=update.message.chat_id, video=video_content, caption=CUSTOM_MESSAGE)
        else:
            image_url = post.url
            image_content = download_content(image_url)
            await context.bot.send_photo(chat_id=update.message.chat_id, photo=image_content, caption=CUSTOM_MESSAGE)
    except Exception as e:
        print(f'Error al descargar el contenido: {e}')

def download_content(url: str) -> io.BytesIO:
    response = requests.get(url, timeout=120)  # Aumentar el tiempo de espera a 120 segundos
    response.raise_for_status()
    content = io.BytesIO(response.content)
    return content

def main() -> None:
    # Crear la aplicación
    app = ApplicationBuilder().token(API_TOKEN).build()

    # Agregar manejadores de comandos
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    # Agregar manejador de mensajes de texto y enlaces
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_message))

    # Iniciar el bot
    app.run_polling()

if __name__ == '__main__':
    main()
