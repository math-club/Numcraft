#   classes.py
#
#   This program is part of NumCraft
#
#
__version__ = "beta 1"
__author__ = [
    "Nathan Duranel",
    "Timéo Arnouts"
]

import random
import re


game_name = "NumCraft"
update_name = "BETA"

help_docs = [("help","show help for commands"),
             ("credits","show credits"),
             ("inv","show inventory"),
             ("player","show infos about current player"),
             ("players","show saved players list"),
             ("ench","buy random enchantment for 10 diamonds"),
             ("quit","quit game"),
             ("god","full inventory"),
             ("save","save current player"),
]


#- CLASS -#

class Quit(Exception):
    """Raised to quit NumCraft"""
    def __init__(self, message: str):
        self.message = message

class EnchantError(Exception):
    """Raised if the enchantment to apply is already applied"""
    def __init__(self, message: str = "Enchantment already applied"):
        self.message = message

class PlayerError(Exception):
    """Raised when a player name or ID is unvalidated"""
    def __init__(self, message: str = "Player name unvalidated"):
        self.message = message

class MainChoiceError(Exception):
    """Raised when main_choice is unvalidated (development purpose)"""
    def __init__(self, message: str = "Error: main_choice unvalidated"):
        self.message = message

class Player:

    def __init__(self,
                 name: str,
                 id: str):
        self.name = name
        self.id = id
        self.current_dimension = 0
        self.y_level = "mine"
        self.inventory = {
            "minerals": {"diamond": [0, 1],
                         "iron": [0, 2],
                         "stone": [0, 1]},
            "surface_ressources": {"wood": [0,1],
                                   "dirt": [0,1]}
        }
        self.enchantments = []

    def get_inventory(self) -> str:
        inventory_string = "%s Inventory" % (self.name)
        for category in self.inventory.items():
            inventory_string += ("%s" % (category.capitalize()) +
                ("\n".join("%s: %s" % (ore.capitalize(), nb[0])
                    for ore, nb in self.inventory[category].items())))

    def add_enchantments(self, enchants:list):
        for enchantment in enchants:
            if enchantment in self.enchantments:
                raise EnchantError
        self.enchantments += enchants

class Commands:

    def ench(player, ressources) -> str:
        """Randomly choose an enchantment to apply
            Cost 10 diamonds
            If the enchantment is already applied, it takes 1 diamond anyway"""
        cost = 10
        min_cost = 1
        rand_ench = random.choices(list(ressources["enchantment"]),[10])[0]
        if player.inventory["minerals"]["diamond"][0] < cost:
            return "Sorry, not enough diamonds"
        try:
            player.add_enchantments([rand_ench])
            player.inventory["minerals"]["diamond"][0] -= cost
            return "Applied %s!" % (rand_ench)
        except EnchantError:
            player.inventory["minerals"]["diamond"][0] -= min_cost

            return ("Sorry, %s already own!\n" % rand_ench
                            + "Maybe you'll get another next time!")

    def quit(player, ressources) -> str:
        """leave game"""
        raise Quit("Thanks for playing, %s." % (player.name))

    def god(player, ressources) -> str:
        """give the player enough minerals"""
        player.inventory["minerals"]["diamond"][0] = 42042
        player.inventory["minerals"]["iron"][0] = 42042
        player.inventory["minerals"]["stone"][0] = 42042

        return "Inventory fulled"

    def save(player, ressources) -> str:
        """
        save current player
        File reading:
        line1 - player.name"todo", "todo"dimension
        line4 - player.y_level
        line5 - player.inventory
        line6 - player.enchantments
        """
        with open("%s.save.numcraft" % (player.id),"w") as save_file:
            data = [player.name, 
                            player.id,
                            player.current_dimension,
                            player.y_level,
                            player.inventory,
                            player.enchantments,]
            save_file.write("\n" .join(list(str(element) for element in data)))
        return "Succesfuly saved %s" % (player.name)

    def move_up(player, ressources) -> str:
        """Move the player 1 y_level up"""
        current = ressources["y_levels"][player.y_level][2]
        try:
            player.y_level = ressources["y_levels_list"][current + 1]
        except IndexError:
            return "%s can't dig up more!" % (player.name)
        return "%s dig up to %s!" % (player.name, player.y_level)

    def move_down(player, ressources) -> str:
        """Move the player 1 y_level down"""
        current = ressources["y_levels"][player.y_level][2]
        try:
            player.y_level = ressources["y_levels_list"][current - 1]
        except IndexError:
            return "%s can't dig down more!" % (player.name)
        return "%s dig down to %s!" % (player.name, player.y_level)


class Indication:

    def intro() -> str:
        return ("%s %s %s. \n" % (game_name,__version__, update_name) +
                        'Type "help" or "credits" for more information.')

    def salutation(player) -> str:
        return "Hi %s." % player.name

    def quotes() -> str:
        splash_text = (
            "Also try Minecraft!",
            "Coding UTF-8!",
            "GG!",
            "The answer is 42",
            "Also try Archess_btw!",
            "Also try Terraria!",
        )

        return "\t" + random.choice(splash_text)

    def help(player) -> str:
        """show help for commands"""
        return ("%s %s %s\n\n" % (game_name,__version__, update_name) +
                        "\n".join(list("%s - %s" % (command,doc)
                            for command,doc in help_docs)))

    def credits(player) -> str:
        """show credits"""
        return "Authors : %s" % ", ".join(__author__)

    def player_infos(player) -> str:
        """show some infos about current player"""
        infos = ("Name: %s" % (player.name),
                         "ID: %s" % (player.id))
        return "Player infos:\n%s" % "\n".join(infos)

    def players_list(player) -> str:
        """show list of players played"""
        with open("id_list.numcraft","r") as id_file:
            id_name_list = id_file.readline().split(" ")
            id_name_list = list(id_name.split("=") for id_name in id_name_list)
            format_id_name_list = []
            for id_name in id_name_list:
                format_id_name_list += [" = " .join(id_name)]
        return ("Players list:" +
                        "\n" .join(format_id_name_list))


#- FUNCTIONS -#

def list_to_str(list_of_str: list) -> str:
    string = ""
    for element in list_of_str:
        string += element
    return string


def generate_id(name) -> str:
    """Generate a new player ID wich isn't already used"""
    with open("id_list.numcraft", "r") as id_list_file:
        id_name_list = ["id0=name0"] + id_list_file.readline().split(" ")
        id_list = list(id_name.split("=")[0] for id_name in id_name_list)
    with open("id_list.numcraft", "w") as id_list_file:
        player_id = "id0"
        while player_id in id_list:
            player_id = list_to_str(list(random.choice(
                ["a", "b", "c", "d", "e", "f"])
                for i in range(8)))
        id_name_list += ["%s=%s" % (player_id, name)]
        id_list_file.write(" " .join(id_name_list[1:]))
    return player_id


def validate_player(name) -> str:
    """Validate a name and return an ID"""
    if re.search(r"^[a-z0-9A-Z._*!]+$", name) is None:
        raise PlayerError('Username accept: "a-Z", "0-9", "._*!"')
    player_id = generate_id(name)
    return player_id


def verify_id(player_id) -> bool:
    with open("id_list.numcraft", "r") as id_file:
        id_name_list = id_file.readline().split(" ")
        id_list = list(id_name.split("=")[0] for id_name in id_name_list)
    return player_id in id_list


def read_save(player_id) -> Player:
    """Read save file and create the player"""
    if not verify_id(player_id):
        raise PlayerError("ID unrecognized")
    with open("%s.save.numcraft" % (player_id), "r") as save_file:
        if not save_file.readable():
            return "Save file corrupted"
        player_name = save_file.readline().rstrip("\n")
        player_id = save_file.readline().rstrip("\n")
        player = Player(player_name, player_id)
        player.current_dimension = eval(save_file.readline().rstrip("\n"))
        player.y_level = save_file.readline().rstrip("\n")
        player.inventory = eval(save_file.readline().rstrip("\n"))
        player.enchantments = eval(save_file.readline().rstrip("\n"))
    return player


def generate_ore(player, ressources):
    if player.current_dimension == 0:
        weight = ressources["y_levels"][player.y_level][0]
        category = ressources["y_levels"][player.y_level][1]
        ore, values = (random.choices(list((ore, values)
                                           for ore, values in player.inventory[category].items()),
                                      weight))[0]
        nb = values[1]
        if "fortune" in player.enchantments:
            nb *= random.choices([2, 3, 4], [60, 30, 10])[0]
    return ore, nb, category
