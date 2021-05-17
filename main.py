# This file is part of the Maxtoan Tools package.
# 
# (c) https://maximosojo.github.io/myhivewallet-bot
# 
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.

# Import configuration
from config import Config
# Import logging
import logging
# Import telegram
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)
# Enable logging
from telegram.utils import helpers

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def start(update, context):
    user = update.message.from_user
    bot_msg = "Saludos {}, bienvenido.\n\n" \
              "¿Que soy?.\n" \
              "Soy el Bot Wallet de Hive, conmigo puede tener en su Telegram un resumen a tiempo real de su wallet en hive. Naci a modo de prueba y mi nacimiendo esta en un post publico en Hive\n\n" \
              "Use el comando /help para conocer las opciones disponibles.\n\n" \
              "La publicación donde naci https://maximosojo.github.io/myhivewallet-bot\n" \
              "Mi código fuente esta en https://maximosojo.github.io/myhivewallet-bot\n" \
              "Perfil de mi creador https://peakd.com/@maximosojo\n\n" \
              "Nota: El bot no registra ningun tipo de información, esto puede ser verificado en su código fuente.\n\n" \
              "Disfrute del bot. Gracias por estar aquí! \n\n".format(user.first_name)
    update.message.reply_text(bot_msg)

def help(update, context):
    """Enviar un mensaje cuando se emite el comando /help"""
    bot_msg = "Comandos disponibles:\n" \
              "/start Inicio del bot\n" \
              "/sumarry Buscar el resumen propio (Busca el resumen segun su nombre de usuario de Telegram)\n" \
              "/search Buscar el resumen de un usuario (Solicita el nombre del usuario a consultar)\n" \
              "/exit Finalizar la conversación con el bot\n"
    update.message.reply_text(bot_msg)

def error(update, context):
    """Log de errors."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    """Configuración inicial de bot."""
    # Registro de token previamente registrado.
    updater = Updater(Config.getBotToken(), use_context=True)

    # Obtiene el event dispatcher para registrar las acciones del bot
    dp = updater.dispatcher

    # Inicia el bot
    dp.add_handler(CommandHandler("start", start))
    
    # Ayuda del bot
    dp.add_handler(CommandHandler("help", help))

    # Retorna errores
    dp.add_error_handler(error)

    # Inicia el bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()