import discord
from discord.ext import commands, tasks
from PIL import ImageDraw, Image
from PIL.ImagePalette import random
from itertools import cycle
import os
import asyncio

intent_used = discord.Intents.all()
intent_used.message_content = True
prefixes = ["!"]
bot = commands.Bot(command_prefix=prefixes, intents=intent_used)

bot_statuses = cycle(["У моего создателя самые кривые руки", "Нил Сисирига!", "*Стикер солдат*", "По запросу 'ТЗ' "
                                                                                                 "ничего не найдено"])

TOKEN = ""


@tasks.loop(seconds=3)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(bot_statuses)))


async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


async def main():
    async with bot:
        await load()
        await bot.start(TOKEN)


@bot.event
async def on_ready():
    print("\n\n=НА СВЯЗИ=\n\n")
    change_status.start()
    await bot.tree.sync()



asyncio.run(main())
