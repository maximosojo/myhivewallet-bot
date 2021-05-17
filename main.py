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
from telegram.ext import (
    Updater,
    CommandHandler
)
# Enable logging
from telegram.utils import helpers
from bs4 import BeautifulSoup
import requests

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Método para busqueda de la data con web scraping
def search_action_resolve(element):
    text = '--'
    d = element.find('div', {'class': 'column small-12 medium-4'})
    if d:
        text = d.text
    return text

# Método para busqueda de la data con web scraping
def search_action(context,username):
    # Inicializando variables
    cont = 0
    account = ''
    hive = hive_power = hive_dollars = savings = total = 0
    is_valid = False
    # Se realiza la busqueda de Data
    parse_url = f'https://wallet.hive.blog/@{username}/transfers'
    url = requests.get(parse_url)
    soup = BeautifulSoup(url.content, 'html.parser')
    results_account = soup.find('h1')
    results = soup.find('div', {'class': 'UserWallet'})
    
    # Se obtiene el nombre del usuario de la cuenta
    if results_account:
        account = results_account.text
    
    # Se recorren los resultados
    if results is not None:
        for result in results:
            if cont == 1:
                hive = search_action_resolve(result)
                is_valid = True
            if cont == 2:
                hive_power = search_action_resolve(result)
            if cont == 3:
                hive_dollars = search_action_resolve(result)
            if cont == 4:
                savings = search_action_resolve(result)
            if cont == 5:
                total = search_action_resolve(result)
            cont = cont + 1
    
    # Se obtiene la data a retornar    
    context.user_data['account'] = account
    context.user_data['hive'] = hive
    context.user_data['hive_power'] = hive_power
    context.user_data['hive_dollars'] = hive_dollars
    context.user_data['savings'] = savings
    context.user_data['total'] = total
    
    return is_valid

def start(update, context):
    user = update.message.from_user
    bot_msg = "Saludos {}, bienvenido.\n\n" \
              "¿Que soy?.\n" \
              "Soy el Bot Wallet de Hive, conmigo puede tener en su Telegram un resumen a tiempo real de su wallet en Hive. Naci a modo de prueba y esta escrito en un post público en Hive\n\n" \
              "Use el comando /help para conocer las opciones disponibles.\n\n" \
              "La publicación donde naci https://github.com/maximosojo/myhivewallet-bot\n" \
              "Mi código fuente esta en https://github.com/maximosojo/myhivewallet-bot\n" \
              "Perfil de mi creador https://peakd.com/@maximosojo\n\n" \
              "Nota: El bot no registra ningun tipo de información, esto puede ser verificado en su código fuente.\n\n" \
              "Disfrute del bot. Gracias por estar aquí! \n\n".format(user.first_name)
    update.message.reply_text(bot_msg)

def help(update, context):
    """Enviar un mensaje cuando se emite el comando /help"""
    bot_msg = "Comandos disponibles:\n" \
              "/start Inicio del bot\n" \
              "/summary Buscar el resumen propio (Busca el resumen segun su nombre de usuario de Telegram)\n" \
              "/exit Finalizar la conversación con el bot\n"
    update.message.reply_text(bot_msg)

def summary(update, context):
    user = update.message.from_user
    is_valid = search_action(context,user.username)
    if is_valid == True:
        """Enviar un mensaje con el resumen de la busqueda"""
        bot_msg = "Saludos {} el resumen de tu Wallet\n\n" \
                  "Hive: {}\n" \
                  "HIVE POWER: {}\n" \
                  "HIVE DOLLARS: {}\n" \
                  "AHORROS: {}\n" \
                  "Valor de cuenta aproximado: {}\n\n" \
                  "Gracias por estar aquí! Creado por @maximosojo".format(context.user_data['account'],context.user_data['hive'],context.user_data['hive_power'],context.user_data['hive_dollars'],context.user_data['savings'],context.user_data['total'])
    else:
        bot_msg = "No fue encontrado el perfil, parece que no es el mismo usuario de Telegram.\n\n" \
            "Gracias por estar aquí! Creado por @maximosojo"
    
    update.message.reply_text(bot_msg)

def exit(update, context):
    update.message.reply_text("exit")

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

    # Resumen del usuario según su usuario de Telegram
    dp.add_handler(CommandHandler("summary", summary))

    # Cierra la conversación con el bot
    dp.add_handler(CommandHandler("exit", exit))

    # Retorna errores
    dp.add_error_handler(error)

    # Inicia el bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()