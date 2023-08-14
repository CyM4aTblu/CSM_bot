# coding=utf-8
from PIL import ImageDraw, Image
import discord
from discord.ext import commands
from discord import app_commands

EMBED_COLOR = discord.Color.from_rgb(77, 235, 229)


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
                            (self.view.bannedMapsCounter == 4 and self.view.winner_in_previous_round != None)):
                        map_choosed_embed = discord.Embed(
                            title=f"Карта  ***{self.view.bannedMapsNumbers}***  была выбрана командой:",
                            description=f"**<@&{self.view.outsiders.id}>**",
                            color=discord.Color.dark_teal()
                        )
                        await interaction.response.send_message(embed=map_choosed_embed)
                        self.view.stop()
                    elif ((self.view.bannedMapsCounter == 2 and self.view.winner_in_previous_round == None) or (self.view.bannedMapsCounter == 5) or
                            (self.view.bannedMapsCounter == 3 and self.view.winner_in_previous_round != None)):
                        if self.view.bannedMapsCounter == 2:
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
    def __init__(self, outsiders, frontRunners, winner_in_previous_round):
        super().__init__()
        self.outsiders = outsiders
        self.frontRunners = frontRunners
        self.activeRole = outsiders
        self.winner_in_previous_round = winner_in_previous_round
        if winner_in_previous_round != None:
            self.activeRole = winner_in_previous_round
            if winner_in_previous_round == outsiders:
                self.outsiders = frontRunnersd
                self.frontRunners = outsiders
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
        "Мегакарп": "Maps_maker.png",
        "Устробол": "Maps_clam.png",
        "Бой за Башню": "Maps_tower.png",
        "Бой за Зоны": "Maps_zones.png"
    }


class ModeBanButton(discord.ui.Button):
    def __init__(self, label):
        super().__init__(label=label, style=discord.ButtonStyle.green)

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.get_role(self.view.outsiders.id) or interaction.user.get_role(self.view.frontRunners.id):
            if (self.view.bannedMode != ""
                    and self.view.bannedMode != self.label
                    and interaction.user.get_role(self.view.outsiders.id)):
                mapView = MapsView(self.view.outsiders, self.view.frontRunners, self.view.winner_in_previous_round)
                mapView.mode = self.label
                if self.view.winner_in_previous_round != None:
                    description_param = (f"<@&{self.view.frontRunners.id}> должна забанить 3 из 8 "
                                         f"карт нажав на сответствующие кнопки\n\n"
                                         f"После чего <@&{self.view.outsiders.id}>"
                                         f" выбирает карту из 3-х оставшихся")
                else:
                    description_param = (f"<@&{self.view.outsiders.id}> должна забанить 2 из 8"
                                                         " карт нажав на сответствующие кнопки\n"
                                                         f"Далее <@&{self.view.frontRunners.id}>"
                                                         f" банит 3 карты из оставшихся\n"
                                                         f"После чего <@&{self.view.outsiders.id}>"
                                                         f" выбирает карту из 3-х оставшихся")
                choose_embed = discord.Embed(title=f"{interaction.user.name} Выбрал режим:  ***{mapView.mode}***",
                                             description= description_param,
                                             colour=EMBED_COLOR)
                choose_embed.set_image(url="attachment://"+mapView.imageUrls[mapView.mode])
                await interaction.response.send_message(file=discord.File(mapView.imageUrls[mapView.mode]),embed=choose_embed, view=mapView)
                self.view.stop()
            elif self.view.bannedMode == "" and interaction.user.get_role(self.view.frontRunners.id):
                self.view.bannedMode = self.label
                self.view.getmodespic(self.label)
                ban_action_embed = discord.Embed(title="Этап №1 - Выбор режима",
                                                 description=f"<@&{self.view.outsiders.id}> выбирает режим из 3-х оставшихся",
                                                 colour=EMBED_COLOR)
                ban_action_embed.set_image(url="attachment://Modes.png")
                self.disabled = True
                self.style = discord.ButtonStyle.gray
                await interaction.response.send_message(file=discord.File("Modes.png"), view=self.view, embed=ban_action_embed)
            else:
                await interaction.response.send_message(
                    f"{interaction.user.name}, сейчас очередь выбирать другой команды, подожди немного!")
        else:
            await interaction.response.send_message(f"{interaction.user.name},"
                                                    f" ты не принадлежишь ни к одной из сражающихся команд!")


class ModesView(discord.ui.View):
    def __init__(self, outsiders, frontRunners, winner_in_previous_round):
        super().__init__()
        self.outsiders = outsiders
        self.winner_in_previous_round = winner_in_previous_round
        self.frontRunners = frontRunners
        self.add_item(ModeBanButton("Бой за Зоны"))
        self.add_item(ModeBanButton("Мегакарп"))
        self.add_item(ModeBanButton("Бой за Башню"))
        self.add_item(ModeBanButton("Устробол"))

    bannedMode = ""

    def getmodespic(self, banned_mode=""):
        modes = Image.open(r"images/templates/Modes.png")
        if banned_mode == "Бой за Зоны":
            cross = Image.open(r"images/crosses/Mode_ban_1.png")
            modes.paste(cross, (0,0), cross)
        elif banned_mode == "Мегакарп":
            cross = Image.open(r"images/crosses/Mode_ban_2.png")
            modes.paste(cross, (0,0), cross)
        elif banned_mode == "Бой за Башню":
            cross = Image.open(r"images/crosses/Mode_ban_3.png")
            modes.paste(cross, (0,0), cross)
        elif banned_mode == "Устробол":
            cross = Image.open(r"images/crosses/Mode_ban_4.png")
            modes.paste(cross, (0,0), cross)
        modes.save("Modes.png")
        return


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

    @app_commands.command(name="start", description="Начать процесс выбора карты")
    @app_commands.describe(team_1="Дискорд-тэг твоей команды", team_2="Дискорд-тэг команды противника",
                           winner_in_previous_round="Укажите Дискорд-тэг команды победившей в последнем РАУНДЕ если уже играли с этими противниками ")
    async def start(self, interaction: discord.Interaction, team_1: discord.Role, team_2: discord.Role, winner_in_previous_round: discord.Role = None):
        for i in self.Teams:
            if i.name == team_1.name:
                outsiders = team_1
                seedOut = i.seed
            elif i.name == team_2.name:
                frontRunners = team_2
                seedRnrs = i.seed
        if ((seedOut > seedRnrs and winner_in_previous_round == None) or
                (winner_in_previous_round == outsiders)):
            outsiders, frontRunners = frontRunners, outsiders
        modeView = ModesView(outsiders, frontRunners, winner_in_previous_round)
        modeView.getmodespic()
        modes_embed = discord.Embed(title="Этап №1 - Выбор режима",
                                    description=f"<@&{frontRunners.id}> должна забанить 1 из 4"
                                                " режимов нажав на сответствующую кнопку\n\n\n",
                                    colour=EMBED_COLOR)
        modes_embed.set_image(url="attachment://Modes.png")
        await interaction.response.send_message(file=discord.File("Modes.png"),embed=modes_embed, view=modeView)


async def setup(bot):
    await bot.add_cog(PickBan(bot))
