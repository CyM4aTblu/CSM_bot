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
        if interaction.user.get_role(self.view.outsiders.id) or interaction.user.get_role(self.view.frontRunners.id):
            if interaction.user.get_role(self.view.activeRole.id):
                if self.view.isBanned[self.label] == True:
                    await interaction.response.send_message(f"***Карта  [{self.label}]  уже была ЗАБАНЕНА***\n"
                                                            f"выберите другую карту")
                else:
                    self.view.bannedMapsNumbers += " [" + self.label + "] "
                    self.view.bannedMapsCounter += 1
                    self.view.isBanned[self.label] = True
                    if (self.view.bannedMapsCounter == 6 or
                            (self.view.bannedMapsCounter == 4 and self.view.Winner_in_Previous_Round != None)):
                        map_choosed_embed = discord.Embed(
                            title=f"Карта  ***{self.view.bannedMapsNumbers}***  была выбрана командой:",
                            description=f"**<@&{self.view.outsiders.id}>**",
                            color=discord.Color.dark_teal()
                        )
                        await interaction.response.send_message(embed=map_choosed_embed)
                        self.view.stop()
                    elif ((self.view.bannedMapsCounter == 2 or self.view.bannedMapsCounter == 5) or
                            (self.view.bannedMapsCounter == 3 and self.view.Winner_in_Previous_Round != None)):
                        if self.view.bannedMapsCounter == 2 or self.view.bannedMapsCounter == 3:
                            self.view.activeRole = self.view.frontRunners
                        else:
                            self.view.activeRole = self.view.outsiders
                        maps_banned_embed = discord.Embed(
                            title=f"{interaction.user.name} Забанил карты:  ***{self.view.bannedMapsNumbers}***",
                            colour=discord.Colour.red())
                        await interaction.response.send_message(embed=maps_banned_embed)
                        self.view.bannedMapsNumbers = ""
                    await interaction.response.edit_message(view=self.view)
            else:
                await interaction.response.send_message(
                    f"{interaction.user.name}, сейчас очередь выбирать другой команды, подожди немного!")
        else:
            await interaction.response.send_message(f"{interaction.user.name},"
                                                    f" ты не принадлежишь ни к одной из сражающихся команд!")


class MapsView(discord.ui.View):
    def __init__(self, outsiders, frontRunners, Winner_in_Previous_Round):
        super().__init__()
        self.outsiders = outsiders
        self.frontRunners = frontRunners
        self.activeRole = outsiders
        self.Winner_in_Previous_Round = Winner_in_Previous_Round
        self.add_item(MapBanButton("1", 1))
        self.add_item(MapBanButton("2", 1))
        self.add_item(MapBanButton("3", 1))
        self.add_item(MapBanButton("4", 1))
        self.add_item(MapBanButton("5", 2))
        self.add_item(MapBanButton("6", 2))
        self.add_item(MapBanButton("7", 2))
        self.add_item(MapBanButton("8", 2))
        self.isBanned = {
            "Pick": False,
            "1": False,
            "2": False,
            "3": False,
            "4": False,
            "5": False,
            "6": False,
            "7": False,
            "8": False,
        }
        self.bannedMapsCounter = 0
        self.bannedMapsNumbers = ""

    mode = ''
    imageUrls = {
        "Мегакарп": "https://media.discordapp.net/attachments/1138780111416606782/1139581216518045817/rainmaker-maps-no-numbers.png?width=875&height=600",
        "Устробол": "https://media.discordapp.net/attachments/1138780111416606782/1139581216996204544/clam-maps-no-numbers.png?width=875&height=600",
        "Бой за Башню": "https://media.discordapp.net/attachments/1138780111416606782/1139581216744550522/tower-maps-no-numbers.png?width=832&height=582",
        "Бой за Зоны": "https://media.discordapp.net/attachments/1138780111416606782/1139581217306574989/zone-maps-no-numbers.png?width=850&height=558"
    }


class ModeBanButton(discord.ui.Button):
    def __init__(self, label):
        super().__init__(label=label, style=discord.ButtonStyle.green)

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.get_role(self.view.outsiders.id) or interaction.user.get_role(self.view.frontRunners.id):
            if (self.view.bannedMode != ""
                    and self.view.bannedMode != self.label
                    and interaction.user.get_role(self.view.outsiders.id)):
                mapView = MapsView(self.view.outsiders, self.view.frontRunners, self.view.Winner_in_Previous_Round)
                mapView.mode = self.label
                choose_embed = discord.Embed(title=f"{interaction.user.name} Выбрал режим:  ***{mapView.mode}***",
                                             description=f"<@&{self.view.outsiders.id}> должна забанить 2 из 8"
                                                         " карт нажав на сответствующие кнопки\n"
                                                         f"Далее <@&{self.view.frontRunners.id}>"
                                                         f" банит 3 карты из оставшихся\n"
                                                         f"После чего <@&{self.view.outsiders.id}>"
                                                         f" выбирает карту из 3-х оставшихся",
                                             colour=discord.Colour.blurple())
                choose_embed.set_image(url=mapView.imageUrls[mapView.mode])
                await interaction.response.send_message(embed=choose_embed, view=mapView)
                self.view.stop()
            elif self.view.bannedMode == "" and interaction.user.get_role(self.view.frontRunners.id):
                self.view.bannedMode = self.label
                ban_action_embed = discord.Embed(
                    title=f"{interaction.user.name} Забанил режим:  ***{self.view.bannedMode}***",
                    colour=discord.Colour.red())
                await interaction.response.send_message(embed=ban_action_embed)
            elif (self.view.bannedMode != "" and interaction.user.get_role(self.view.frontRunners.id)) or (
                    self.view.bannedMode == "" and interaction.user.get_role(self.view.outsiders.id)):
                await interaction.response.send_message(
                    f"{interaction.user.name}, сейчас очередь выбирать другой команды, подожди немного!")
            else:
                await interaction.response.send_message(
                    f"{interaction.user.name}, этот режим уже был забанен, **ITS NO USE!**")
        else:
            await interaction.response.send_message(f"{interaction.user.name},"
                                                    f" ты не принадлежишь ни к одной из сражающихся команд!")


class ModesView(discord.ui.View):
    def __init__(self, outsiders, frontRunners, Winner_in_Previous_Round):
        super().__init__()
        self.outsiders = outsiders
        self.Winner_in_Previous_Round = Winner_in_Previous_Round
        self.frontRunners = frontRunners
        self.add_item(ModeBanButton("Бой за Зоны"))
        self.add_item(ModeBanButton("Мегакарп"))
        self.add_item(ModeBanButton("Бой за Башню"))
        self.add_item(ModeBanButton("Устробол"))

    bannedMode = ""


class PickBan(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    Teams = [
        Team("Sync", 1, 2),
        Team("Чай", 2, 3),
        Team("Floyd", 3, 4),
        Team("Гей&Дроч", 0, 8)
    ]

    @commands.Cog.listener()
    async def on_ready(self):
        print("PickBan - online")

    @app_commands.command(name="battle", description="Начать процесс выбора карты")
    @app_commands.describe(Team_1="Дискорд-тэг твоей команды", Team_2="Дискорд-тэг команды противника",
                           Winner_in_Previous_Round="Играли ли вы с командой противников в этом матче? \n"
                                                    "если НЕТ - оставьте поле пустым\n"
                                                    "если ДА - укажите Дискорд-тэг команды"
                                                    " победившей в последнем РАУНДЕ")
    async def battle(self, interaction: discord.Interaction,
                     Team_1: discord.Role, Team_2: discord.Role, Winner_in_Previous_Round: discord.Role = None):
        for i in self.Teams:
            if i.name == Team_1.name:
                outsiders = Team_1
                seedOut = i.seed
            elif i.name == Team_2.name:
                frontRunners = Team_2
                seedRnrs = i.seed
        if ((seedOut > seedRnrs and Winner_in_Previous_Round == None) or
                (Winner_in_Previous_Round.name == outsiders.name)):
            outsiders, frontRunners = frontRunners, outsiders
        modeView = ModesView(outsiders, frontRunners, Winner_in_Previous_Round)
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
