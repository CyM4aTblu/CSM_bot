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
            # проерка принадлежности к одной из 2х команд
            if interaction.user.get_role(self.view.activeRole.id):
                # проверка на принадлежность к команде, чья сейчас очередь выирать карты
                if self.view.isBanned[self.label] == True:
                    await interaction.response.send_message(f"***Карта  [{self.label}]  уже была ЗАБАНЕНА***\n"
                                                            f"выберите другую карту", ephemeral=True)
                else:
                    # процедура бана карты и обновленя картинки
                    self.view.bannedMapsNumbers += " [" + self.label + "] "
                    self.view.bannedMapsCounter += 1
                    self.view.isBanned[self.label] = True
                    self.disabled = True
                    self.style = discord.ButtonStyle.gray
                    self.view.getmapspic()
                    if (self.view.bannedMapsCounter == 6 or
                            (self.view.bannedMapsCounter == 4 and self.view.winner_in_previous_round != None)):
                        # выбор карты
                        map_choosed_embed = discord.Embed(
                            title=f"Карта  ***{self.view.bannedMapsNumbers}***  была выбрана командой:",
                            description=f"**<@&{self.view.outsiders.id}>**",
                            color=EMBED_COLOR
                        )
                        map_choosed_embed.set_image(url="attachment://Win.png")
                        await interaction.response.send_message(file=discord.File("Win.png"), embed=map_choosed_embed)
                        self.view.stop()
                    else:
                        #  бан карты
                        discr = f"Очередь команды **<@&{self.view.activeRole.id}>** забанитть очередную карту!"
                        if self.view.bannedMapsCounter == 2 and self.view.winner_in_previous_round == None:
                            self.view.activeRole = self.view.frontRunners
                            discr = f"Очередь команды **<@&{self.view.activeRole.id}>** забанитть очередную карту!"
                        elif ((self.view.bannedMapsCounter == 3 and self.view.winner_in_previous_round != None) or
                              (self.view.bannedMapsCounter == 5)):
                            self.view.activeRole = self.view.outsiders
                            discr = f"Очередь команды **<@&{self.view.activeRole.id}>** выбрать карту из оствшихся!"
                        maps_banned_embed = discord.Embed(
                            title=f"{interaction.user.name} Забанил карты:  ***{self.view.bannedMapsNumbers}***",
                            description=discr,
                            colour=EMBED_COLOR)
                        maps_banned_embed.set_image(url="attachment://"+self.view.imageUrls[self.view.mode])
                        await interaction.response.send_message(file=discord.File(self.view.imageUrls[self.view.mode]), embed=maps_banned_embed, view=self.view)
                        self.view.bannedMapsNumbers = ""
                    await interaction.response.edit_message(view=self.view)
            else:
                await interaction.response.send_message(
                    f"{interaction.user.name}, сейчас очередь выбирать другой команды, подожди немного!",
                    ephemeral=True)
        else:
            await interaction.response.send_message(f"{interaction.user.name},"
                                                    f" ты не принадлежишь ни к одной из сражающихся команд!",
                                                    ephemeral=True)


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


    def getmapspic(self):  # функция редакирования картинки с картами
        end_path = self.imageUrls[self.mode]
        start_path = "images/templates/" + end_path
        maps = Image.open(start_path)
        for i in range(1,9):
            ind = str(i)
            if self.isBanned[ind]:
                cross = Image.open("images/crosses/Maps_ban_" + ind + ".png")
                maps.paste(cross, (0, 0), cross)
        numbers = Image.open(r"images/templates/Mode_numbers.png")
        maps.paste(numbers, (0, 0), numbers)
        maps.save(end_path)



class ModeBanButton(discord.ui.Button):
    def __init__(self, label):
        super().__init__(label=label, style=discord.ButtonStyle.green)

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.get_role(self.view.outsiders.id) or interaction.user.get_role(self.view.frontRunners.id):
            # проерка принадлежности к одной из 2х команд
            if (self.view.bannedMode != ""
                    and self.view.bannedMode != self.label
                    and interaction.user.get_role(self.view.outsiders.id)):
                # проерка на то, не был ли забанен режим
                mapView = MapsView(self.view.outsiders, self.view.frontRunners, self.view.winner_in_previous_round)
                mapView.mode = self.label
                mapView.getmapspic()
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
                    f"{interaction.user.name}, сейчас очередь выбирать другой команды, подожди немного!"
                    , ephemeral=True)
        else:
            await interaction.response.send_message(f"{interaction.user.name},"
                                                    f" ты не принадлежишь ни к одной из сражающихся команд!",
                                                    ephemeral=True)


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

    def getmodespic(self, banned_mode=""):# функция динамического изменения картинки с режимами
        modes = Image.open(r"images/templates/Modes.png")
        if banned_mode == "Бой за Зоны":
            cross = Image.open(r"images/crosses/Mode_ban_1.png")
        elif banned_mode == "Мегакарп":
            cross = Image.open(r"images/crosses/Mode_ban_2.png")
        elif banned_mode == "Бой за Башню":
            cross = Image.open(r"images/crosses/Mode_ban_3.png")
        elif banned_mode == "Устробол":
            cross = Image.open(r"images/crosses/Mode_ban_4.png")
        if banned_mode != "":
            modes.paste(cross, (0,0), cross)
        modes.save("Modes.png")
        return


class PickBan(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # бд команд с их сидингами
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
                           last_winner="Укажите Дискорд-тэг команды одержавшей победу в прошлом БОЮ [НЕ ПРИМЕНИМО К ПЕРВОМУ БОЮ В СЭТЕ]")
    async def start(self, interaction: discord.Interaction, team_1: discord.Role, team_2: discord.Role, last_winner: discord.Role = None):
        if interaction.user.get_role(team_1.id) or interaction.user.get_role(team_2.id):
            # проерка принадлежности к одной из 2х команд
            for i in self.Teams:
                if i.name == team_1.name:
                    outsiders = team_1
                    seedOut = i.seed
                elif i.name == team_2.name:
                    frontRunners = team_2
                    seedRnrs = i.seed
            if ((seedOut > seedRnrs and last_winner == None) or
                    (last_winner == outsiders)):
                outsiders, frontRunners = frontRunners, outsiders
            # процедура определения команды аутсайдера и фаворита ^
            modeView = ModesView(outsiders, frontRunners, last_winner)
            modeView.getmodespic()
            modes_embed = discord.Embed(title="Этап №1 - Выбор режима",
                                        description=f"<@&{frontRunners.id}> должна забанить 1 из 4"
                                                    " режимов нажав на сответствующую кнопку\n\n\n",
                                        colour=EMBED_COLOR)
            modes_embed.set_image(url="attachment://Modes.png")
            await interaction.response.send_message(file=discord.File("Modes.png"),embed=modes_embed, view=modeView)
        else:
            await interaction.response.send_message(f"Ты не состоишь ни в одной из этих 2-х команд,"
                                                    f" ***{interaction.user.name}***!\nНи к  <@&{team_1.id}>,"
                                                    f" ни к <@&{team_2.id}>", ephemeral=True)
async def setup(bot):
    await bot.add_cog(PickBan(bot))
