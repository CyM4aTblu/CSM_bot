import discord
from discord.ext import commands
# концепт каточки команды, идея аналогична с карточкой игрока
"""
class Team:
    def __init__(self, _name, players, repacePlayers, discordNames, role, iconUrl):
        self.name = _name
        self.players = players
        self.repacePlayers = repacePlayers
        self.discordNames = discordNames
        self.roleId = role
        self.iconUrl = iconUrl
"""

class TeamCard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("TeamCard - online")

    @commands.hybrid_command(description="Отображет карточку запрашиваемой команды")
    async def team(self, ctx):
        embed_message = discord.Embed(title="Заголовок",
                                      description="Описание",
                                      colour=discord.Colour.green())
        embed_message.set_author(name=f"По запросу {ctx.author.name}", icon_url=ctx.author.avatar)
        embed_message.set_thumbnail(url=ctx.guild.icon)
        embed_message.set_image(url=ctx.author.avatar)
        embed_message.add_field(name="Мейн оружия", value="Текст поля", inline=True)
        embed_message.add_field(name="Сила X", value="Мегакарп = ~\nБой за Башню = ~\nБой за зоны = ~\nУстрабол = ~",
                                inline=True)
        embed_message.set_footer(text="Видать эта снизу", icon_url=
        'https://media.discordapp.net/attachments/994356082313023560/1139184279318958231/9zmu3VCQfSM.png?width=600&height=450')

        await ctx.send(embed=embed_message)


async def setup(bot):
    await bot.add_cog(TeamCard(bot))