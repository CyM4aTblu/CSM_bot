import discord
from discord.ext import commands
from discord import app_commands


class ChatCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("ChatCommands - online")

    @commands.hybrid_command()
    async def hello(self, ctx):
        await ctx.send("Здарова, щегол!")

    @app_commands.command(name="square", description="powers int into a square")
    async def square(self, interaction: discord.Interaction, number: int):
        await interaction.response.send_message(number**2)


async def setup(bot):
    await bot.add_cog(ChatCommands(bot))