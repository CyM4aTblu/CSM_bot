# coding=utf-8
import discord
from discord.ext import commands
from discord import app_commands


class Team:
    def __init__(self, name, seed, tag):
        self.name = name
        self.seed = seed
        self.tag = tag


class MapsView(discord.ui.View):
    mode = ''
    imageUrls = {
        "Мегакарп": "https://media.discordapp.net/attachments/1138780111416606782/1139581216518045817/rainmaker-maps-no-numbers.png?width=875&height=600",
        "Устробол": "https://media.discordapp.net/attachments/1138780111416606782/1139581216996204544/clam-maps-no-numbers.png?width=875&height=600"
    }

    @discord.ui.button(label="1", style=discord.ButtonStyle.primary)
    async def first(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("ЖЕСТОКО НАДРИСТАЛ")

    @discord.ui.button(label="2", style=discord.ButtonStyle.primary)
    async def serondMap(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("ЖЕСТОКО НАДРИСТАЛ")

    @discord.ui.button(label="3", style=discord.ButtonStyle.primary)
    async def thirdMap(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("ЖЕСТОКО НАДРИСТАЛ")

    @discord.ui.button(label="4", style=discord.ButtonStyle.primary)
    async def fourthMap(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("ЖЕСТОКО НАДРИСТАЛ")

    @discord.ui.button(label="5", style=discord.ButtonStyle.primary)
    async def fifthMap(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("ЖЕСТОКО НАДРИСТАЛ")

    @discord.ui.button(label="6", style=discord.ButtonStyle.primary)
    async def sixthMap(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("ЖЕСТОКО НАДРИСТАЛ")

    @discord.ui.button(label="7", style=discord.ButtonStyle.primary)
    async def seventhMap(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("ЖЕСТОКО НАДРИСТАЛ")

    @discord.ui.button(label="8", style=discord.ButtonStyle.primary)
    async def eighthMap(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("ЖЕСТОКО НАДРИСТАЛ")


class ModesView(discord.ui.View):
    bannedMode = ""

    @discord.ui.button(label="Мегакарп", style=discord.ButtonStyle.primary)
    async def RainmakerButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.bannedMode != "" and self.bannedMode != "Мегакарп":
            mapView = MapsView()
            mapView.mode = "Мегакарп"
            choose_embed = discord.Embed(title=f"{interaction.user.name} Выбрал режим:  ***Мегакарп***",
                                         description="***ИМЯ КОМАНДЫ С НИЗКИМ СИДОМ*** должна забанить 2 из 8"
                                                  " карт нажав на сответствующие кнопки\n"
                                                  "Далее ***ИМЯ КОМАНДЫ С ВЫСОКИМ СИДОМ*** банит 3 карты из оставшихся\n"
                                                  "После чего ***ИМЯ КОМАНДЫ С НИЗКИМ СИДОМ*** выбирает карту из 3-х оставшихся",
                                         colour=discord.Colour.blurple())
            choose_embed.set_image(url=mapView.imageUrls["Мегакарп"])
            await interaction.response.send_message(embed=choose_embed, view=mapView)
            self.stop()
        elif self.bannedMode != "Мегакарп":
            self.bannedMode = "Мегакарп"
            ban_action_embed = discord.Embed(title=f"{interaction.user.name} Забанил режим:  ***{self.bannedMode}***",
                                             colour=discord.Colour.red())
            await interaction.response.send_message(embed=ban_action_embed)
        else:
            #await interaction.response.send_message(view=mapView)
            await interaction.response.send_message(f"{interaction.user.name}, этот режим уже был забанен, **ITS NO USE!**")

    @discord.ui.button(label="Бой за Башню", style=discord.ButtonStyle.success)
    async def TowerControlButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.bannedMode != "" and self.bannedMode != "Бой за Башню":
            choose_embed = discord.Embed(title=f"{interaction.user.name} Выбрал режим:  ***Бой за Башню***",
                                         colour=discord.Colour.blurple())
            await interaction.response.send_message(embed=choose_embed)
            self.stop()
        elif self.bannedMode != "Бой за Башню":
            self.bannedMode = "Бой за Башню"
            ban_action_embed = discord.Embed(title=f"{interaction.user.name} Забанил режим:  ***{self.bannedMode}***",
                                             colour=discord.Colour.red())
            await interaction.response.send_message(embed=ban_action_embed)
        else:
            await interaction.response.send_message(
                f"{interaction.user.name}, этот режим уже был забанен, **ITS NO USE!**")

    @discord.ui.button(label="Устробол", style=discord.ButtonStyle.secondary)
    async def ClamBlitzButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.bannedMode != "" and self.bannedMode != "Устробол":
            choose_embed = discord.Embed(title=f"{interaction.user.name} Выбрал режим:  ***Устробол***",
                                         colour=discord.Colour.blurple())
            await interaction.response.send_message(embed=choose_embed)
            self.stop()
        elif self.bannedMode != "Устробол":
            self.bannedMode = "Устробол"
            ban_action_embed = discord.Embed(title=f"{interaction.user.name} Забанил режим:  ***{self.bannedMode}***",
                                             colour=discord.Colour.red())
            await interaction.response.send_message(embed=ban_action_embed)
        else:
            await interaction.response.send_message(
                f"{interaction.user.name}, этот режим уже был забанен, **ITS NO USE!**")

    @discord.ui.button(label="Бой за Зоны", style=discord.ButtonStyle.red)
    async def SplatZonesButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.bannedMode != "" and self.bannedMode != "Бой за Зоны":
            choose_embed = discord.Embed(title=f"{interaction.user.name} Выбрал режим:  ***Бой за Зоны***",
                                         colour=discord.Colour.blurple())
            await interaction.response.send_message(embed=choose_embed)
            self.stop()
        elif self.bannedMode != "Бой за Зоны":
            self.bannedMode = "Бой за Зоны"
            ban_action_embed = discord.Embed(title=f"{interaction.user.name} Забанил режим:  ***{self.bannedMode}***",
                                             colour=discord.Colour.red())
            await interaction.response.send_message(embed=ban_action_embed)
        else:
            await interaction.response.send_message(
                f"{interaction.user.name}, этот режим уже был забанен, **ITS NO USE!**")

class PickBan(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("PickBan - online")

    @app_commands.command(name="start", description="Начать процесс выбора карты")
    async def start(self, interaction: discord.Interaction):
        modeView = ModesView()

        modes_embed = discord.Embed(title="Этап №1 - Выбор режима",
                                      description="***ИМЯ КОМАНДЫ С ВЫСОКИМ СИДОМ*** должна забанить 1 из 4"
                                                  " режимов нажав на сответствующую кнопку\n\n\n"
                                                  "После чего ***ИМЯ КОМАНДЫ С НИЗКИМ СИДОМ*** выбирает режим из 3-х оставшихся",
                                      colour=discord.Colour.gold())
        modes_embed.set_image(url=
        "https://media.discordapp.net/attachments/994356082313023560/1139622287717437600/FQ_v1XwXMAA-v8G.png?width=972&height=670")
        await interaction.response.send_message(embed=modes_embed, view=modeView)
        #await modeView.wait()


async def setup(bot):
    await bot.add_cog(PickBan(bot))