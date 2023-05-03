'''
메인 파일
'''
import discord
from discord.ext import commands
from keumjeong import LOGGER, TOKEN, EXTENSIONS, BOT_NAME, BOT_TAG, email_password, email_id
import sys
from keumjeong.cogs.email import EmailVerifyButton

class keumjeongbot(commands.AutoShardedBot):
    '''Main Class'''

    def __init__(self):
        super().__init__(
            intents=intents
        )
        self.persistent_views_added = False
        self.remove_command("help")
        for i in EXTENSIONS:
            self.load_extension("keumjeong.cogs." + i)

    async def on_ready(self):
        '''봇 준비 이벤트'''
        self.bot = bot  # pylint: disable=W0201
        if not self.persistent_views_added:
            self.add_view(EmailVerifyButton(self.bot))
            self.persistent_views_added = True
        LOGGER.info('Archive Clan Bot#2327 | V.3.2')
        LOGGER.info("""[%s#%s] v1.0\n[Python] v%s\n[Py-Cord] v%s""" % (BOT_NAME,BOT_TAG,sys.version,discord.__version__))  # pylint: disable=E1101


intents = discord.Intents.all()

bot = keumjeongbot()
bot.run(TOKEN)
