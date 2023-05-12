import random
import discord
from discord.ext import commands
from discord.commands import slash_command, Option
import motor.motor_asyncio
from keumjeong import LOGGER, color_code, DebugServer
from keumjeong.utils.mail_sender import mail_sender
import datetime

dbclient = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
db = dbclient.keumjeong

class Student_Info_Modal(discord.ui.Modal):
    '''EmailinfoModal'''

    def __init__(self, bot, *args, **kwargs) -> None:
        super().__init__(
            discord.ui.InputText(
                label="학번과 이름을 입력해주세요.",
                placeholder="1101 홍길동",
                required=True
            ),
            title="재학생 인증",
            *args,
            **kwargs)
        self.bot = bot
        self.color = color_code
        self.student_id = None
        self.interaction_msg = None

    async def callback(self, interaction: discord.Interaction):
        '''EmailinfoModal Callback'''
        self.student_id = self.children[0].value
        self.interaction_msg = await interaction.response.send_message('잠시만 기다려주세요..', ephemeral=True)

class EmailVerifyButton(discord.ui.View):
    '''캡챠 버튼'''

    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot
        self.color_code = color_code

    @discord.ui.button(label="재학생 인증", style=discord.ButtonStyle.primary, custom_id='email::verify')
    async def captcha(self, button, interaction: discord.Interaction):  # pylint: disable=W0613
        teacher = False # 선생님 유무
        email_modal = Student_Info_Modal(self.bot)
        await interaction.response.send_modal(email_modal)
        await email_modal.wait()

        interactionmsg = email_modal.interaction_msg
        studentid = email_modal.student_id
    
        if len(studentid.split(" ")[0]) == 5 and 't' in studentid.split(" ")[0]:
            teacher=True
            number2 = studentid.split(" ")[0] # 선생님 메일
            name = studentid.split(" ")[1] # 선생님 이름
        elif len(studentid.split(" ")) >= 3 or len(studentid.split(" ")) <= 1 or len(studentid.split(" ")[0]) != 4 or len(studentid.split(" ")[1]) >= 5 or len(studentid.split(" ")[1]) <= 1: # 학번 제대로 입력했는지 확인
            await interactionmsg.edit_original_response(content='학번과 이름을 제대로 입력해주세요.')
            return
        else:
            number2 = studentid.split(" ")[0] # 학번
            name = studentid.split(" ")[1] # 이름

        grade = list(number2)[0]
        if grade == '1':
            grade_r = 1097727965128839169
        elif grade == '2':
            grade_r = 1097727998477750352
        elif grade == '3':
            grade_r = 1097728026051092497
        else:
            await interactionmsg.edit_original_response(content="인증에 실패하셨습니다.", embed=None, view=None)
            
        code = str(random.randint(10000, 99999)) # 코드 생성
        r_code = mail_sender(number2,code) # 코드 메일 전송

        if r_code == 'success': # 메일 전송 성공 시
            async def check(interaction):
                global MSG
                await interaction.response.send_message('입력 중....', ephemeral=True, delete_after = 0)
                inputtype = interaction.custom_id.split("-")[1]
                code2 = MSG.embeds[0].to_dict()["description"].split("\n ")[-1].replace("```","").replace("-","").replace(" ","")

                if inputtype=="del" and len(code) > 0: # Backspace 버튼 처리
                    result = code2[:-1]
                elif inputtype=="clear" and len(code) > 0: # 클리어 버튼 처리
                    result = ''
                elif inputtype!="del": # 일반 버튼 처리
                    result = code2 + inputtype
                else:
                    await interactionmsg.edit_original_response()
                    return
                
                if len(result) == 5:
                    realcode=button_d.custom_id.split("-")[2]
                    if result==realcode:
                        await interactionmsg.edit_original_response(content="인증이 완료되었습니다.", embed=None,view=None)
                        if teacher == False:
                            role = interaction.guild.get_role(grade_r)
                            role2 = interaction.guild.get_role(1097728080811917322)
                            await interaction.user.add_roles(role)
                            await interaction.user.remove_roles(role2)
                            await interaction.user.edit(nick=number2)
                            await interactionmsg.edit_original_response(content="인증이 완료되었습니다.", embed=None,view=None)
                            db.user_data.insert_one({"number": number2, "name": name, "date": datetime.datetime.now()}) # date 는 인증시각
                        elif teacher == True:
                            role = interaction.guild.get_role(1097727933298245673)
                            role2 = interaction.guild.get_role(1097728080811917322)
                            await interaction.user.add_roles(role)
                            await interaction.user.remove_roles(role2)
                            await interaction.user.edit(nick=number2.split(" ")[1])
                            await interactionmsg.edit_original_response(content="인증이 완료되었습니다.", embed=None,view=None)
                            db.user_data.insert_one({"number": number2, "name": name, "date": datetime.datetime.now()}) # date 는 인증시각

                    else:
                        await interactionmsg.edit_original_response(content="인증에 실패하셨습니다.", embed=None,view=None)
                else:
                    MSG = await interactionmsg.edit_original_response(
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
            MSG = await interactionmsg.edit_original_response(content=None,embed=embed, view=view)
        else: # 메일 전송 실패 시
            await interactionmsg.edit_original_response(content='현재는 이메일 인증을 시도하실 수 없습니다. 관리자에게 문의주세요.')

class StudentVerify(commands.Cog):
    '''메인 클래스'''

    def __init__(self, bot):
        self.bot = bot

    @slash_command(name='인증설정', DebugServer=DebugServer)
    async def captcha(self, ctx,
                      text: Option(str, 
                                   description="임베드에 들어갈 설명을 입력해주세요.",
                                   required=True),
                      channel: Option(discord.TextChannel, 
                                      description="캡챠가 설정될 채널을 설정해주세요.",
                                      required=True)):
        '''Verify Setting'''
        studentverify_setting = discord.Embed(title="재학생 인증", description=text, color=color_code)
        messgae_id = await self.bot.get_channel(channel.id).send(embed=studentverify_setting, 
                                                                 view=EmailVerifyButton(self.bot))
        db.verify.insert_one({"channel": channel.id, "message": messgae_id, "description": text})
        await ctx.respond(f'{channel.mention} 설정 완료')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        '''member join 확인 함수'''
        role = member.guild.get_role(1097728080811917322)
        await member.add_roles(role)
        await member.edit(nick='미인증 학생')

def setup(bot):
    '''cogs setup 함수'''
    bot.add_cog(StudentVerify(bot))
    LOGGER.info('StudentVerify loaded!')
