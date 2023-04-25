'''
메인 파일
'''
import discord
from discord.ext import commands
from keumjeong import LOGGER, TOKEN, EXTENSIONS, BOT_NAME, BOT_TAG
import sys
from keumjeong.cogs.email import EmailVerifyButton
# from oauth2client.service_account import ServiceAccountCredentials
# import gspread

# scope = [
# 'https://spreadsheets.google.com/feeds',
# 'https://www.googleapis.com/auth/drive',
# ]
# json_file_name = './key.json'
# credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
# gc = gspread.authorize(credentials)
# spreadsheet_url = 'https://docs.google.com/spreadsheets/d/19Eimpldlq-9Wi52BY_bE-z0jTvq0H1gcygFWKL_jHDY/edit#gid=0'
# doc = gc.open_by_url(spreadsheet_url)
# worksheet = doc.worksheet('Sheet1')
#gs = gc.create('새로운 테스트')
#worksheet = gs.add_worksheet(title='시트1', rows='1', cols='1')
#gs.share('kimjw2198@gmail.com', perm_type='user', role='writer')
# list_of_lists = worksheet.get_all_values()
# print(list_of_lists)

class timecheckbot(commands.AutoShardedBot):
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
#intents.guilds = True

bot = timecheckbot()
bot.run(TOKEN)
