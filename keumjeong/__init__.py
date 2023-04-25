'''
init
'''
import os
import logging
from keumjeong.config import Development as Config

BOT_VER = "V.3.2"
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)
LOGGER = logging.getLogger(__name__)
TOKEN = Config.TOKEN
OWNERS = Config.OWNERS
DebugServer = Config.DebugServer
BOT_NAME = Config.BOT_NAME
BOT_TAG = Config.BOT_TAG
BOT_ID = Config.BOT_ID
color_code = Config.color_code
error_cc = Config.error_cc

EXTENSIONS = []
for file in os.listdir("keumjeong/cogs"):
    if file.endswith(".py"):
        EXTENSIONS.append(file.replace(".py", ""))