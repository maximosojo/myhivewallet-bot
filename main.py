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