import random
import datetime
import discord
from discord.ext import commands
from discord.commands import slash_command, Option
import motor.motor_asyncio
from keumjeong import LOGGER, color_code, DebugServer
from keumjeong.utils.mail_sender import mail_sender

dbclient = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
db = dbclient.blacklist
class code_check(discord.ui.Modal):
    '''TaskModal'''

    def __init__(self, bot, *args, **kwargs) -> None:
        super().__init__(
            discord.ui.InputText(
                label="학번과 이름을 입력해주세요.",
                placeholder="1101 홍길동",
                required=True
            ),
            title="Task Setting",
            *args,
            **kwargs)
        self.bot = bot
        self.color = color_code
        self.code2 = None

    async def callback(self, interaction: discord.Interaction):
        '''Task Modal Callback'''
        self.code2 = self.children[0].value
        self.interactionmsg = await interaction.response.send_message(f'잠시만 기다려주세요.', ephemeral=True)

class email_info(discord.ui.Modal):
    '''TaskModal'''

    def __init__(self, bot, *args, **kwargs) -> None:
        super().__init__(
            discord.ui.InputText(
                label="학번과 이름을 입력해주세요.",
                placeholder="1101 홍길동",
                required=True
            ),
            title="Task Setting",
            *args,
            **kwargs)
        self.bot = bot
        self.color = color_code
        self.number = None
        self.interactionmsg = None

    async def callback(self, interaction: discord.Interaction):
        '''Task Modal Callback'''
        self.number = self.children[0].value
        self.interactionmsg = await interaction.response.send_message('잠시만 기다려주세요..', ephemeral=True)
        
class EmailVerifyButton(discord.ui.View):
    '''캡챠 버튼'''

    def __init__(self, bot):
        super().__init__(timeout=None)
        self.persistent_views_added = False
        self.bot = bot
        self.color_code = color_code

    @discord.ui.button(label="재학생 인증", style=discord.ButtonStyle.primary, custom_id='email::verify')
    async def captcha(self, button, interaction: discord.Interaction):  # pylint: disable=W0613
        t = False # 선생님 유무
        email_modal = email_info(self.bot)
        await interaction.response.send_modal(email_modal)
        await email_modal.wait()

        if len(email_modal.number.split(" ")[0]) == 5 and 't' in email_modal.number.split(" ")[0]:
            t=True
            number2 = email_modal.number.split(" ")[0] # 선생님 메일
            name = email_modal.number.split(" ")[1] # 선생님 이름
        elif len(email_modal.number.split(" ")) >= 3 or len(email_modal.number.split(" ")) <= 1 or len(email_modal.number.split(" ")[0]) != 4 or len(email_modal.number.split(" ")[1]) >= 5 or len(email_modal.number.split(" ")[1]) <= 1: # 학번 제대로 입력했는지 확인
            await email_modal.interactionmsg.edit_original_response(content='학번과 이름을 제대로 입력해주세요.')
            return
        else:
            number2 = email_modal.number.split(" ")[0] # 학번
            name = email_modal.number.split(" ")[1] # 이름

        grade = list(number2)[0]
        if grade == '1':
            grade_r = 1097727965128839169
        elif grade == '2':
            grade_r = 1097727998477750352
        elif grade == '3':
            grade_r = 1097728026051092497
        else:
            await email_modal.interactionmsg.edit_original_response(content="인증에 실패하셨습니다.", embed=None, view=None)
            
        c_list = [] # 코드 생성
        code = str(random.randint(10000, 99999)) # 알맞는 코드
        c_list.append(code)
        r_code = mail_sender(number2,code) # 코드 메일 전송

        if r_code == 'success': # 메일 전송 성공 시

            async def check(interaction):
                await interaction.response.send_message('입력 중....', ephemeral=True, delete_after = 0)
                global MSG
                type = interaction.custom_id.split("-")[1]
                code2 = MSG.embeds[0].to_dict()["description"].split("\n ")[-1].replace("```","").replace("-","").replace(" ","")

                if type=="del" and len(code) > 0: # Backspace 버튼 처리
                    result = code2[:-1]
                elif type=="clear" and len(code) > 0: # 클리어 버튼 처리
                    result = ''
                elif type!="del": # 일반 버튼 처리
                    result = code2 + type
                else:
                    await email_modal.interactionmsg.edit_original_response()
                    return
                
                if len(result) == 5:
                    realCode=button_d.custom_id.split("-")[2]
                    if result==realCode:
                        await email_modal.interactionmsg.edit_original_response(content="인증이 완료되었습니다.", embed=None,view=None)
                    else:
                        await email_modal.interactionmsg.edit_original_response(content="인증에 실패하셨습니다.", embed=None,view=None)
                else:
                    MSG = await email_modal.interactionmsg.edit_original_response(
                        embed = discord.Embed(title="재학생 인증",description=f"`{number2}@keumjeong.hs.kr` 로 전송된 코드가 적힌 버튼을 눌러주세요.\n\n```\n - {result}```",color=color_code))
            
            view = discord.ui.View()
            button_c = discord.ui.Button(style=discord.ButtonStyle.red,label='Clear',custom_id="captcha-clear",row=3)
            button_0 = discord.ui.Button(style=discord.ButtonStyle.blurple,emoji="\U00000030\U0000FE0F\U000020E3",custom_id="captcha-0",row=3)
            button_d = discord.ui.Button(style=discord.ButtonStyle.red,emoji="\U0001F519",custom_id=f"captcha-del-{code}-{interaction.user.id}",row=3)
            button_1 = discord.ui.Button(style=discord.ButtonStyle.blurple,emoji="\U00000031\U0000FE0F\U000020E3",custom_id="captcha-1",row=2)
            button_2 = discord.ui.Button(style=discord.ButtonStyle.blurple,emoji="\U00000032\U0000FE0F\U000020E3",custom_id="captcha-2",row=2)
            button_3 = discord.ui.Button(style=discord.ButtonStyle.blurple,emoji="\U00000033\U0000FE0F\U000020E3",custom_id="captcha-3",row=2)
            button_4 = discord.ui.Button(style=discord.ButtonStyle.blurple,emoji="\U00000034\U0000FE0F\U000020E3",custom_id="captcha-4",row=1)
            button_5 = discord.ui.Button(style=discord.ButtonStyle.blurple,emoji="\U00000035\U0000FE0F\U000020E3",custom_id="captcha-5",row=1)
            button_6 = discord.ui.Button(style=discord.ButtonStyle.blurple,emoji="\U00000036\U0000FE0F\U000020E3",custom_id="captcha-6",row=1)
            button_7 = discord.ui.Button(style=discord.ButtonStyle.blurple,emoji="\U00000037\U0000FE0F\U000020E3",custom_id="captcha-7",row=0)
            button_8 = discord.ui.Button(style=discord.ButtonStyle.blurple,emoji="\U00000038\U0000FE0F\U000020E3",custom_id="captcha-8",row=0)
            button_9 = discord.ui.Button(style=discord.ButtonStyle.blurple,emoji="\U00000039\U0000FE0F\U000020E3",custom_id="captcha-9",row=0)
            view.add_item(button_c)
            view.add_item(button_0)
            view.add_item(button_1)
            view.add_item(button_2)
            view.add_item(button_3)
            view.add_item(button_4)
            view.add_item(button_5)
            view.add_item(button_6)
            view.add_item(button_7)
            view.add_item(button_8)
            view.add_item(button_9)
            view.add_item(button_d)
            button_c.callback = check
            button_0.callback = check
            button_1.callback = check
            button_2.callback = check
            button_3.callback = check
            button_4.callback = check
            button_5.callback = check
            button_6.callback = check
            button_7.callback = check
            button_8.callback = check
            button_9.callback = check
            button_d.callback = check

            global MSG
            embed = discord.Embed(title='재학생 인증',description=f"`{number2}@keumjeong.hs.kr` 로 전송된 코드가 적힌 버튼을 눌러주세요.\n\n```\n -```",color=color_code)                
            MSG = await email_modal.interactionmsg.edit_original_response(content=None,embed=embed, view=view)
        else: # 메일 전송 실패 시
            await email_modal.interactionmsg.edit_original_response(content='현재는 이메일 인증을 시도하실 수 없습니다. 관리자에게 문의주세요.')
        

class captcha(commands.Cog):
    '''메인 클래스'''

    def __init__(self, bot):
        self.bot = bot

    @slash_command(name='인증설정', DebugServer=DebugServer)
    async def captcha(self, ctx, text: Option(str, description="임베드에 들어갈 설명을 입력해주세요.", required=True), channel: Option(discord.TextChannel, description="캡챠가 설정될 채널을 설정해주세요.", required=True)):
        clanregister = discord.Embed(title="재학생 인증", description=text, color=color_code)
        a = await self.bot.get_channel(channel.id).send(embed=clanregister, view=EmailVerifyButton(self.bot))
        a = str(a.id)
        cha = str(channel.id)
        text = str(text)
        db.captcha.insert_one({"channel": cha, "message": a, "description": text})
        await ctx.respond(f'{channel.mention} 설정 완료')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        '''member join 확인 함수'''
        role = member.guild.get_role(1097728080811917322)
        await member.add_roles(role)
        await member.edit(nick='미인증 학생')


def setup(bot):
    '''cogs setup 함수'''
    bot.add_cog(captcha(bot))
    LOGGER.info('Email loaded!')