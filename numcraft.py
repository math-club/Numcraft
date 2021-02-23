#  numcraft.py
#
#  Copyright 2021 Nathan Duranel, Timéo Arnouts
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#
__version__ = "beta 0.6"
__author__ = [
  "Nathan Duranel",
  "Timéo Arnouts"
]


import random


game_name = "Numcraft"
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


def capitalize(string: str) -> str:
  return string[0].upper() + string[1:]

def list_to_str(list_of_str: list) -> str:
  string = ""
  for element in list_of_str:
    string += element
  return string

def weight_choice(choices_list: list, weight: list):
  if len(choices_list) == len(weight):
    weighted=[]
    for i in range(len(choices_list)):
      weighted += list(choices_list[i] for x in range(weight[i]))
    return random.choice(weighted)
  else:
      raise ValueError(("In Function: weight_choices() - "
                    "len(choices_list) and len(weight) must be equals"))

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
    return "\n".join("%s: %s" % (capitalize(ore), nb[0])
                     for ore, nb in self.inventory["minerals"].items())

  def add_enchantments(self, enchants:list):
    for i in enchants:
      if i in self.enchantments:
        raise EnchantError
    self.enchantments += enchants

class Commands:

  def ench(player,ressources) -> str:
    """Randomly choose an enchantment to apply
      Cost 10 diamonds
      If the enchantment is already applied, it takes 1 diamond anyway"""
    cost = 10
    min_cost = 1
    rand_ench = weight_choice(list(ressources["enchantment"]),[10])
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

  def quit(player,ressources) -> str:
    """leave game"""
    raise Quit("Thanks for playing, %s." % (player.name))

  def god(player,ressources) -> str:
    """give the player enough minerals"""
    player.inventory["minerals"]["diamond"][0] = 42042
    player.inventory["minerals"]["iron"][0] = 42042
    player.inventory["minerals"]["stone"][0] = 42042

    return "Inventory fulled"

  def save(player,ressources) -> str:
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
      "Also try Archess_btw!"
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


def generate_id(name) -> str:
  """Generate a new player ID wich isn't already used"""
  with open("id_list.numcraft","r") as id_list_file:
    id_name_list = ["id0=name0"] + id_list_file.readline().split(" ")
    id_list = list(id_name.split("=")[0] for id_name in id_name_list)
  with open("id_list.numcraft","w") as id_list_file:
    player_id = "id0"
    while player_id in id_list:
      player_id = list_to_str(list(random.choice(["a","b","c","d","e","f"])
        for i in range(8)))
    id_name_list += ["%s=%s" % (player_id,name)]
    print(id_list)
    id_list_file.write(" " .join(id_name_list[1:]))
  return player_id

def validate_player(name) -> str:
  """Validate a name and return an ID"""
  unwanted = " ", "="
  for character in name:
    if character in unwanted:
      raise PlayerError('No spaces or "=" in player name')
  player_id = generate_id(name)
  return player_id

def verify_id(player_id) -> bool:
  with open("id_list.numcraft","r") as id_file:
    id_name_list = id_file.readline().split(" ")
    id_list = list(id_name.split("=")[0] for id_name in id_name_list)
  return player_id in id_list

def read_save(player_id) -> Player:
  """Read save file and create the player"""
  if not verify_id(player_id):
    raise PlayerError("ID unrecognized")
  with open("%s.save.numcraft" % (player_id),"r") as save_file:
    if not save_file.readable():
      return "Save file corrupted"
    player_name = save_file.readline().rstrip("\n")
    player_id = save_file.readline().rstrip("\n")
    player = Player(player_name,player_id)
    player.current_dimension = eval(save_file.readline().rstrip("\n"))
    player.y_level = save_file.readline().rstrip("\n")
    player.inventory = eval(save_file.readline().rstrip("\n"))
    player.enchantments = eval(save_file.readline().rstrip("\n"))
  return player

def generate_ore(player,y_levels):
  if player.current_dimension == 0:
    if player.y_level == "mine":
      weight = y_levels[player.y_level]
      ore,values = weight_choice(list(
        (ore,values) for ore,values in player.inventory["minerals"].items()),
          weight)
      nb = values[1]
      if "fortune" in player.enchantments:
        nb *= weight_choice([2,3,4],[60,30,10])
    if player.y_level == "surface":
      weight = y_levels[player.y_level]
      ore,values = weight_choice(list(
        (ore,values) for ore,values in player.inventory["minerals"].items()),
          weight)
      nb = values[1]
  return ore,nb


def mainloop():
  commands = {
    "ench": Commands.ench,
    "quit": Commands.quit,
    "god": Commands.god,
    "save": Commands.save,
  }

  indications = {
    "help": Indication.help,
    "credits": Indication.credits,
    "inv": Player.get_inventory,
    "player": Indication.player_infos,
    "players": Indication.players_list,
  }
  
  ressources = {
    "enchantment": {"fortune",}
  }

  y_levels = {
    "surface": [20,80],
    "caves": [1,15,84],
    "mine": [1,10,89]
  }

  player_defined = 0

  try:
    open("id_list.numcraft","r").close()
  except FileNotFoundError:
    open("id_list.numcraft","w").close()

  print(Indication.intro())
  print(Indication.quotes() + "\n")

  main_choice = 0
  while not (main_choice == "n" or main_choice == "c"):
    main_choice = input("n: New Player c: Charge Player [n/c]: ")

  if main_choice == "n":
    while not player_defined:
      try:
        player_name = input("Choose a name: ")
        player_id = validate_player(player_name)
        player_defined = 1
      except PlayerError as player_error:
        print(player_error.args[0])
    player = Player(player_name,player_id)

  elif main_choice == "c":
    print(Indication.players_list(None))
    player_id = 0
    file_exist = 0
    while not verify_id(player_id) or not file_exist:
      player_id = input("Enter ID ")
      if not verify_id(player_id):
        print("Unrecognized ID")
      try:
        open("%s.save.numcraft" % (player_id),"r")
      except FileNotFoundError:
        print("Save file not saved, deleted or bad-named")
      else:
        file_exist = 1
    player = read_save(player_id)

  else:
    raise MainChoiceError()

  print(Indication.salutation(player))

  while 1:
    cmd = input("> ").strip()

    if cmd in commands:
      print(commands[cmd](player,ressources))
    elif cmd in indications:
      print(indications[cmd](player))
    else:
      ore, nb = generate_ore(player,y_levels)
      player.inventory["minerals"][ore][0] += nb

      print(capitalize(ore) + "!")

mainloop()
