import discord
from discord.ext import commands, tasks
from itertools import cycle
import os
import asyncio

# инициализаця параметров бота
intent_used = discord.Intents.all()
intent_used.message_content = True
prefixes = "!"
bot = commands.Bot(command_prefix=prefixes, intents=intent_used)
# статусы бота котрые сменяются поочередно
bot_statuses = cycle(["У моего создателя самые \"прямые\" руки", "Нил Сисирига!", "*Стикер солдат*",
                      "У моих заказчиков самые демократичные сроки", "АМ-НЯМ", "Подпичывайтесь на эвКАЛиптовое дерево!",
                      "=Добро и Позитив=", "Мой исходный код доступен на GitHub!", "Я проиграл в \"игру\"...",
                      "Есть что сказать автору бота? милости прошу в личку: cym4atblu"])
# токен для доступа к аккаунту бота
TOKEN = ""


@tasks.loop(seconds=15)  # функция цикличной смены статусов
async def change_status():
    await bot.change_presence(activity=discord.Game(next(bot_statuses)))


async def load():  # функция загрузки файлов с командами (cogs)
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


async def main():  # функция запуска бота
    async with bot:
        await load()
        await bot.start(TOKEN)


@bot.event
async def on_ready():
    print("\n\n=НА СВЯЗИ=\n\n")
    change_status.start()
    await bot.tree.sync()


asyncio.run(main())
