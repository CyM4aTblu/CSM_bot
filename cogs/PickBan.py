# coding=utf-8
import discord
from discord.ext import commands
from discord import app_commands


class Team:
    def __init__(self, name, seed, tag):
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
        if self.view.bannedMapsCounter == 2 or self.view.bannedMapsCounter == 5:
            maps_banned_embed = discord.Embed(
                title=f"{interaction.user.name} Забанил карты:  ***{self.view.bannedMapsNumbers}***",
                colour=discord.Colour.red())
            await interaction.response.edit_message(view=self.view)
            await interaction.response.send_message(embed=maps_banned_embed)
            self.view.bannedMapsNumbers = ""
        await interaction.response.edit_message(view=self.view)

class MapsView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(MapBanButton("BTN", 1))

    mode = ''
    imageUrls = {
        "Мегакарп": "https://media.discordapp.net/attachments/1138780111416606782/1139581216518045817/rainmaker-maps-no-numbers.png?width=875&height=600",
        "Устробол": "https://media.discordapp.net/attachments/1138780111416606782/1139581216996204544/clam-maps-no-numbers.png?width=875&height=600",
        "Бой за Башню": "https://media.discordapp.net/attachments/1138780111416606782/1139581216744550522/tower-maps-no-numbers.png?width=832&height=582",
        "Бой за Зоны": "https://media.discordapp.net/attachments/1138780111416606782/1139581217306574989/zone-maps-no-numbers.png?width=850&height=558"
    }
    bannedMapsCounter = 0
    bannedMapsNumbers = ""

    def createMapBanButton(self, number: str, row=1):
        @discord.ui.button(label=number, style=discord.ButtonStyle.primary, row=row)
        async def mapBanButton(interaction: discord.Interaction, button: discord.ui.Button):
            self.bannedMapsNumbers += " [" + button.label + "] "
            self.bannedMapsCounter += 1
            if self.bannedMapsCounter == 2 or self.bannedMapsCounter == 5:
                maps_banned_embed = discord.Embed(
                    title=f"{interaction.user.name} Забанил карты:  ***{self.bannedMapsNumbers}***",
                    colour=discord.Colour.red())
                button.disabled = True
                button.style = discord.ButtonStyle.grey
                await interaction.response.send_message(embed=maps_banned_embed)
                self.bannedMapsNumbers = ""
            button.disabled = True
            button.style = discord.ButtonStyle.grey
            await interaction.response.edit_message(view=self)

        return mapBanButton

    @discord.ui.button(label="map2", style=discord.ButtonStyle.primary, row=1)
    async def fdv(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.bannedMapsNumbers += " [" + button.label + "] "
        self.bannedMapsCounter += 1
        if self.bannedMapsCounter == 2 or self.bannedMapsCounter == 5:
            maps_banned_embed = discord.Embed(
                title=f"{interaction.user.name} Забанил карты:  ***{self.bannedMapsNumbers}***",
                colour=discord.Colour.red())
            button.disabled = True
            button.style = discord.ButtonStyle.grey
            await interaction.response.send_message(embed=maps_banned_embed)
            self.bannedMapsNumbers = ""
        button.disabled = True
        button.style = discord.ButtonStyle.grey
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="map1", style=discord.ButtonStyle.primary, row=1)
    async def fdwrv(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.bannedMapsNumbers += " [" + button.label + "] "
        self.bannedMapsCounter += 1
        if self.bannedMapsCounter == 2 or self.bannedMapsCounter == 5:
            maps_banned_embed = discord.Embed(
                title=f"{interaction.user.name} Забанил карты:  ***{self.bannedMapsNumbers}***",
                colour=discord.Colour.red())
            button.disabled = True
            button.style = discord.ButtonStyle.grey
            await interaction.response.send_message(embed=maps_banned_embed)
            self.bannedMapsNumbers = ""
        button.disabled = True
        button.style = discord.ButtonStyle.grey
        await interaction.response.edit_message(view=self)


class ModesView(discord.ui.View):
    bannedMode = ""

    @discord.ui.button(label="Мегакарп", style=discord.ButtonStyle.primary)
    async def RainmakerButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.bannedMode != "" and self.bannedMode != "Мегакарп":
            mapView = MapsView()
            mapView.mode = "Мегакарп"
            choose_embed = discord.Embed(title=f"{interaction.user.name} Выбрал режим:  ***{mapView.mode}***",
                                         description="***ИМЯ КОМАНДЫ С НИЗКИМ СИДОМ*** должна забанить 2 из 8"
                                                     " карт нажав на сответствующие кнопки\n"
                                                     "Далее ***ИМЯ КОМАНДЫ С ВЫСОКИМ СИДОМ*** банит 3 карты из оставшихся\n"
                                                     "После чего ***ИМЯ КОМАНДЫ С НИЗКИМ СИДОМ*** выбирает карту из 3-х оставшихся",
                                         colour=discord.Colour.blurple())
            choose_embed.set_image(url=mapView.imageUrls[mapView.mode])
            await interaction.response.send_message(embed=choose_embed, view=mapView)
            self.stop()
        elif self.bannedMode != "Мегакарп":
            self.bannedMode = "Мегакарп"
            ban_action_embed = discord.Embed(title=f"{interaction.user.name} Забанил режим:  ***{self.bannedMode}***",
                                             colour=discord.Colour.red())
            await interaction.response.send_message(embed=ban_action_embed)
        else:
            # await interaction.response.send_message(view=mapView)
            await interaction.response.send_message(
                f"{interaction.user.name}, этот режим уже был забанен, **ITS NO USE!**")

    @discord.ui.button(label="Бой за Башню", style=discord.ButtonStyle.success)
    async def TowerControlButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.bannedMode != "" and self.bannedMode != "Бой за Башню":
            mapView = MapsView()
            mapView.mode = "Бой за Башню"
            choose_embed = discord.Embed(title=f"{interaction.user.name} Выбрал режим:  ***{mapView.mode}***",
                                         description="***ИМЯ КОМАНДЫ С НИЗКИМ СИДОМ*** должна забанить 2 из 8"
                                                     " карт нажав на сответствующие кнопки\n"
                                                     "Далее ***ИМЯ КОМАНДЫ С ВЫСОКИМ СИДОМ*** банит 3 карты из оставшихся\n"
                                                     "После чего ***ИМЯ КОМАНДЫ С НИЗКИМ СИДОМ*** выбирает карту из 3-х оставшихся",
                                         colour=discord.Colour.blurple())
            choose_embed.set_image(url=mapView.imageUrls[mapView.mode])
            await interaction.response.send_message(embed=choose_embed, view=mapView)
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
            mapView = MapsView()
            mapView.mode = "Устробол"
            choose_embed = discord.Embed(title=f"{interaction.user.name} Выбрал режим:  ***{mapView.mode}***",
                                         description="***ИМЯ КОМАНДЫ С НИЗКИМ СИДОМ*** должна забанить 2 из 8"
                                                     " карт нажав на сответствующие кнопки\n"
                                                     "Далее ***ИМЯ КОМАНДЫ С ВЫСОКИМ СИДОМ*** банит 3 карты из оставшихся\n"
                                                     "После чего ***ИМЯ КОМАНДЫ С НИЗКИМ СИДОМ*** выбирает карту из 3-х оставшихся",
                                         colour=discord.Colour.blurple())
            choose_embed.set_image(url=mapView.imageUrls[mapView.mode])
            await interaction.response.send_message(embed=choose_embed, view=mapView)
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
            mapView = MapsView()
            mapView.mode = "Бой за Зоны"
            choose_embed = discord.Embed(title=f"{interaction.user.name} Выбрал режим:  ***{mapView.mode}***",
                                         description="***ИМЯ КОМАНДЫ С НИЗКИМ СИДОМ*** должна забанить 2 из 8"
                                                     " карт нажав на сответствующие кнопки\n"
                                                     "Далее ***ИМЯ КОМАНДЫ С ВЫСОКИМ СИДОМ*** банит 3 карты из оставшихся\n"
                                                     "После чего ***ИМЯ КОМАНДЫ С НИЗКИМ СИДОМ*** выбирает карту из 3-х оставшихся",
                                         colour=discord.Colour.blurple())
            choose_embed.set_image(url=mapView.imageUrls[mapView.mode])
            await interaction.response.send_message(embed=choose_embed, view=mapView)
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
        # await modeView.wait()


async def setup(bot):
    await bot.add_cog(PickBan(bot))
