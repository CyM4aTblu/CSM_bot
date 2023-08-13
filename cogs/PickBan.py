# coding=utf-8
import discord
from discord.ext import commands
from discord import app_commands


class Team:
    def __init__(self, name, seed, tag: discord.Role):
        self.name = name
        self.seed = seed
        self.tag = tag


class MapBanButton(discord.ui.Button):
    def __init__(self, label, row):
        super().__init__(label=label, style=discord.ButtonStyle.primary, row=row)

    async def callback(self, interaction: discord.Interaction):
        self.view.bannedMapsNumbers += " [" + self.label + "] "
        self.view.bannedMapsCounter += 1
        self.disabled = True
        self.style = discord.ButtonStyle.grey
        if self.view.bannedMapsCounter == 6:
            map_choosed_embed = discord.Embed(title=f"Карта  ***{self.view.bannedMapsNumbers}***  была выбрана командой:",
                description=f"**<@&{self.view.outsiders.id}>**",
                color= discord.Color.dark_teal()
            )
            await interaction.response.send_message(embed=map_choosed_embed) #FIXME: баг не обновления статуса кнопки (невозможность использовать множество interaction.response)
            self.view.stop()
        elif self.view.bannedMapsCounter == 2 or self.view.bannedMapsCounter == 5:
            maps_banned_embed = discord.Embed(
                title=f"{interaction.user.name} Забанил карты:  ***{self.view.bannedMapsNumbers}***",
                colour=discord.Colour.red())
            await interaction.response.send_message(embed=maps_banned_embed)
            self.view.bannedMapsNumbers = ""
        await interaction.response.edit_message(view=self.view)


class MapsView(discord.ui.View):
    def __init__(self, outsiders, frontRunners):
        super().__init__()
        self.outsiders = outsiders
        self.frontRunners = frontRunners
        self.add_item(MapBanButton("1", 1))
        self.add_item(MapBanButton("2", 1))
        self.add_item(MapBanButton("3", 1))
        self.add_item(MapBanButton("4", 1))
        self.add_item(MapBanButton("5", 2))
        self.add_item(MapBanButton("6", 2))
        self.add_item(MapBanButton("7", 2))
        self.add_item(MapBanButton("8", 2))

    mode = ''
    imageUrls = {
        "Мегакарп": "https://media.discordapp.net/attachments/1138780111416606782/1139581216518045817/rainmaker-maps-no-numbers.png?width=875&height=600",
        "Устробол": "https://media.discordapp.net/attachments/1138780111416606782/1139581216996204544/clam-maps-no-numbers.png?width=875&height=600",
        "Бой за Башню": "https://media.discordapp.net/attachments/1138780111416606782/1139581216744550522/tower-maps-no-numbers.png?width=832&height=582",
        "Бой за Зоны": "https://media.discordapp.net/attachments/1138780111416606782/1139581217306574989/zone-maps-no-numbers.png?width=850&height=558"
    }
    bannedMapsCounter = 0
    bannedMapsNumbers = ""


class ModeBanButton(discord.ui.Button):
    def __init__(self, label, style):
        super().__init__(label=label, style=style)

    async def callback(self, interaction: discord.Interaction):
        if self.view.bannedMode != "" and self.view.bannedMode != self.label:
            mapView = MapsView(self.view.outsiders, self.view.frontRunners)
            mapView.mode = self.label
            choose_embed = discord.Embed(title=f"{interaction.user.name} Выбрал режим:  ***{mapView.mode}***",
                                         description=f"<@&{self.view.outsiders.id}> должна забанить 2 из 8"
                                                     " карт нажав на сответствующие кнопки\n"
                                                     f"Далее <@&{self.view.frontRunners.id}> банит 3 карты из оставшихся\n"
                                                     f"После чего <@&{self.view.outsiders.id}> выбирает карту из 3-х оставшихся",
                                         colour=discord.Colour.blurple())
            choose_embed.set_image(url=mapView.imageUrls[mapView.mode])
            await interaction.response.send_message(embed=choose_embed, view=mapView)
            self.view.stop()
        elif self.view.bannedMode != self.label:
            self.view.bannedMode = self.label
            ban_action_embed = discord.Embed(title=f"{interaction.user.name} Забанил режим:  ***{self.view.bannedMode}***",
                                             colour=discord.Colour.red())
            await interaction.response.send_message(embed=ban_action_embed)
        else:
            await interaction.response.send_message(
                f"{interaction.user.name}, этот режим уже был забанен, **ITS NO USE!**")


class ModesView(discord.ui.View):
    def __init__(self, outsiders, frontRunners):
        super().__init__()
        self.outsiders = outsiders
        self.frontRunners = frontRunners
        self.add_item(ModeBanButton("Мегакарп", discord.ButtonStyle.primary))
        self.add_item(ModeBanButton("Бой за Башню", discord.ButtonStyle.green))
        self.add_item(ModeBanButton("Устробол", discord.ButtonStyle.secondary))
        self.add_item(ModeBanButton("Бой за Зоны", discord.ButtonStyle.red))

    bannedMode = ""

class PickBan(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    Teams = [
        Team("Sync", 1, 2),
        Team("Чай", 2, 3),
        Team("Floyd", 3, 4)
    ]

    @commands.Cog.listener()
    async def on_ready(self):
        print("PickBan - online")

    @app_commands.command(name="start", description="Начать процесс выбора карты")
    @app_commands.describe(team1="Дискорд-тэг твоей команды", team2="Дискорд-тэг команды противника")
    async def start(self, interaction: discord.Interaction, team1: discord.Role, team2: discord.Role): #TODO: красивое название параметров вввода
        for i in self.Teams:
            if i.name == team1.name:
                outsiders = team1
                seedOut = i.seed
            elif i.name == team2.name:
                frontRunners = team2
                seedRnrs = i.seed
        if seedOut > seedRnrs:
            outsiders, frontRunners = frontRunners, outsiders
        modeView = ModesView(outsiders, frontRunners)
        modes_embed = discord.Embed(title="Этап №1 - Выбор режима",
                                    description=f"<@&{frontRunners.id}> должна забанить 1 из 4"
                                                " режимов нажав на сответствующую кнопку\n\n\n"
                                                f"После чего <@&{outsiders.id}> выбирает режим из 3-х оставшихся",
                                    colour=discord.Colour.gold())
        modes_embed.set_image(url=
                              "https://media.discordapp.net/attachments/994356082313023560/1139622287717437600/FQ_v1XwXMAA-v8G.png?width=972&height=670")
        await interaction.response.send_message(embed=modes_embed, view=modeView)


async def setup(bot):
    await bot.add_cog(PickBan(bot))
