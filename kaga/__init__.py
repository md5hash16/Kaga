"""Initial app framework"""

import logging
import os
import sys
import time
import spamwatch
import telegram.ext as tg
from telethon import TelegramClient
from dotenv import load_dotenv

StartTime = time.time()

# enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("kaga-log.txt"),
        logging.StreamHandler(),
    ],
    level=logging.INFO,
)

LOGGER = logging.getLogger(__name__)

# if version < 3.6, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    LOGGER.error(
        "You MUST have a python version of at least 3.6!!!."
    )
    sys.exit(1)

load_dotenv("config.env")

CONFIG_CHECK = os.environ.get(
    "_____REMOVE_____THIS_____LINE_____") or None

if CONFIG_CHECK:
    LOGGER.info(
        "Please remove the line mentioned in the first hashtag from the config.env file"
    )
    sys.exit(1)

TOKEN = os.environ.get("TOKEN")
OWNER_ID = int(os.environ.get("OWNER_ID") or 0)
MESSAGE_DUMP = os.environ.get("MESSAGE_DUMP") or None
GBAN_LOGS = os.environ.get("GBAN_LOGS") or None
OWNER_USERNAME = os.environ.get("OWNER_USERNAME") or None
DEV_USERS = set(int(x) for x in os.environ.get("DEV_USERS", "").split())
SUDO_USERS = set(int(x) for x in os.environ.get("SUDO_USERS", "").split())
SUPPORT_USERS = set(
    int(x) for x in os.environ.get(
        "SUPPORT_USERS",
        "").split())
WHITELIST_USERS = set(
    int(x) for x in os.environ.get(
        "WHITELIST_USERS",
        "").split())
WHITELIST_CHATS = set(
    int(x) for x in os.environ.get(
        "WHITELIST_CHATS",
        "").split())
BLACKLIST_CHATS = set(
    int(x) for x in os.environ.get(
        "BLACKLIST_CHATS",
        "").split())
WEBHOOK = bool(os.environ.get("WEBHOOK")) or False
URL = os.environ.get("URL", "")
PORT = int(os.environ.get("PORT", 5000))
CERT_PATH = os.environ.get("CERT_PATH") or None
DB_URI = os.environ.get("DATABASE_URL")
MONGO_URI = os.environ.get("MONGO_DB_URI")
API_ID = os.environ.get('API_ID', None)
API_HASH = os.environ.get('API_HASH', None)
EVENT_LOGS = os.environ.get('EVENT_LOGS', None)
JOIN_LOGGER = os.environ.get('JOIN_LOGGER') or None
DONATION_LINK = os.environ.get("DONATION_LINK") or None
LOAD = os.environ.get("LOAD", "").split()
NO_LOAD = os.environ.get("NO_LOAD", "").split()
SUPPORT_CHAT = os.environ.get('SUPPORT_CHAT', None)
DEL_CMDS = bool(os.environ.get("DEL_CMDS")) or False
STRICT_GBAN = bool(os.environ.get("STRICT_GBAN")) or False
WORKERS = int(os.environ.get("WORKERS", 8))
BAN_STICKER = os.environ.get("BAN_STICKER", "CAACAgQAAx0CSIsLDQACORpf4wqgqJc9c1TFa0Mi_mqItZE2KwACfgEAAj2wWQa-nzvcrdrGrR4E")
CUSTOM_CMD = os.environ.get("CUSTOM_CMD") or False
API_WEATHER = os.environ.get("API_OPENWEATHER") or None
TIME_API_KEY = os.environ.get('TIME_API_KEY', None)
CASH_API_KEY = os.environ.get("CASH_API_KEY") or None
WALL_API = os.environ.get("WALL_API") or None
SPAMWATCH = os.environ.get("SPAMWATCH_API") or None
LASTFM_API_KEY = os.environ.get("LASTFM_API_KEY") or None

# add owner to devusers
DEV_USERS.add(OWNER_ID)

# Pass if SpamWatch token not set.
if SPAMWATCH is None:
    spamwtc = None # pylint: disable=C0103
    LOGGER.warning("Invalid spamwatch api")
else:
    spamwtc = spamwatch.Client(SPAMWATCH)

# Everything Init with this
updater = tg.Updater(TOKEN, workers=WORKERS)
telethn = TelegramClient("kulionlinebot", API_ID, API_HASH)
dispatcher = updater.dispatcher

# Declare user rank
DEV_USERS = list(DEV_USERS)
SUDO_USERS = list(SUDO_USERS)
SUPPORT_USERS = list(SUPPORT_USERS)

STAFF = DEV_USERS + SUDO_USERS + SUPPORT_USERS
STAFF_USERS = list(STAFF)

WHITELIST_USERS = list(WHITELIST_USERS)


# Load at end to ensure all prev variables have been set
# pylint: disable=C0413
from kaga.modules.helper_funcs.handlers import (
    CustomCommandHandler,
)

if CUSTOM_CMD and len(CUSTOM_CMD) >= 1:
    tg.CommandHandler = CustomCommandHandler
