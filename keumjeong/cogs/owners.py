import discord

from discord.ext import commands, pages
from discord.commands import slash_command
from keumjeong import LOGGER, color_code, EXTENSIONS, DebugServer


class Owners (commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_members = None
        self.color = color_code
        self.error_color = 0xff4a4a

    @slash_command(guild_ids=DebugServer)
    @discord.default_permissions(administrator=True)
    async def load(self, ctx, module):
        """ 모듈을 로드합니다. """
        try:
            self.bot.load_extension("blacklistbot.cogs." + module)
            LOGGER.info(f"로드 성공!\n모듈 : {module}")
            embed = discord.Embed(
                title="로드 성공!",
                description=f"모듈 : {module}",
                color=self.color
            )
            if f"*~~{module}~~*" in EXTENSIONS:
                EXTENSIONS[EXTENSIONS.index(f"*~~{module}~~*")] = module
            else:
                EXTENSIONS.append(module)
        except Exception as error:
            LOGGER.error(f"로드 실패!\n에러 : {error}")
            embed = discord.Embed(
                title=f"모듈 : {module}",
                description=f"에러 : {error}",
                color=self.error_color
            )
        await ctx.respond(embed=embed)

    @slash_command(guild_ids=DebugServer)
    @discord.default_permissions(administrator=True)
    async def reload(self, ctx, module):
        """ 모듈을 리로드합니다. """
        try:
            self.bot.reload_extension("blacklistbot.cogs." + module)
            LOGGER.info(f"리로드 성공!\n모듈 : {module}")
            embed = discord.Embed(
                title="리로드 성공!",
                description=f"모듈 : {module}",
                color=self.color
            )
        except Exception as error:
            LOGGER.error(f"리로드 실패!\n에러 : {error}")
            embed = discord.Embed(
                title="리로드 실패!",
                description=f'에러 : {error}',
                color=self.error_color
            )
            if module in EXTENSIONS:
                EXTENSIONS[EXTENSIONS.index(module)] = f"*~~{module}~~*"
        await ctx.respond(embed=embed)

    @slash_command(guild_ids=DebugServer)
    @discord.default_permissions(administrator=True)
    async def unload(self, ctx, module):
        """ 모듈을 언로드합니다. """
        try:
            self.bot.unload_extension("blacklistbot.cogs." + module)
            LOGGER.info(f"언로드 성공!\n모듈 : {module}")
            embed = discord.Embed(
                title="언로드 성공!",
                description=f"모듈 : {module}",
                color=self.color
            )
            if module in EXTENSIONS:
                EXTENSIONS[EXTENSIONS.index(module)] = f"*~~{module}~~*"
        except Exception as error:
            LOGGER.error(f"언로드 실패!\n에러 : {error}")
            embed = discord.Embed(
                title="언로드 실패!",
                description=f'에러 : {error}',
                color=self.error_color
            )
        await ctx.respond(embed=embed)

    @slash_command(guild_ids=DebugServer)
    @discord.default_permissions(administrator=True)
    async def module_list(self, ctx):
        """ 모든 모듈들의 이름을 알려줘요! """
        modulenum = 0
        for m in EXTENSIONS:
            if not m[0:3] == "*~~":
                modulenum += 1
        modulenum = f"{modulenum}개의 모듈들이 로드되어 있습니다."
        e1 = "\n".join(EXTENSIONS)
        embed = discord.Embed(title="**모듈 리스트**", color=color_code)
        embed.add_field(name=modulenum, value=e1, inline=False)
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(Owners(bot))
    LOGGER.info('Owners Loaded!')