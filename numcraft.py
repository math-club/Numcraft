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
__version__ = "beta 0.4"
__author__ = [
  "Nathan Duranel",
  "Timéo Arnouts"
]


import random


game_name = "Numcraft"
update_name = "Code update"


def capitalize(string: str) -> str:
  return string[0].upper() + string[1:]


def weight_choice(choices_list: list, weight: list):
  if len(choices_list) == len(weight):
    weighted=[]
    for i in range(len(choices_list)):
      weighted += list(choices_list[i] for x in range(weight[i]))
    return random.choice(weighted)
  else:
      raise ValueError(("In Function: weight_choices() - "
                    "len(choices_list) and len(weight) must be equals"))

class Error(Exception):
  """NumCraft's exceptions"""
  pass

class Quit(Error):
  """Raised to quit NumCraft"""
  def __init__(self, message) -> None:
      self.message = message


class Player:

  def __init__(self,
               name: str):
    self.name = name
    self.current_dimension = 0

    self.inventory = {
      "minerals": {"diamond": [0, 1],
                   "iron": [0, 2],
                   "stone": [0, 1]}
    }
    self.enchantments = []

  def get_inventory(self) -> str:
    return "\n".join("%s: %s" % (capitalize(ore), nb[0])
                     for ore, nb in self.inventory["minerals"].items())

  def add_enchantments(self, enchants:list):
    for i in enchants:
      if i in self.enchantments:
        raise ValueError
    self.enchantments += enchants

  def get_enchantments(self) -> list:
    return self.enchantments


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
    except ValueError:
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
    """show this message"""
    return ("%s %s %s\n\n" % (game_name,__version__, update_name) +
            "\n".join("%s - %s" % ("todo", "todo")))

  def credits(player) -> str:
    """show credits"""
    return "Authors : %s" % ", ".join(__author__)



def generate_ore(player):
  if player.current_dimension == 0:
    ore,values = weight_choice(list(
      (ore,values) for ore,values in player.inventory["minerals"].items()),[1,10,89])
    nb = values[1]
    if "fortune" in player.get_enchantments():
      nb *= weight_choice([2,3,4],[60,30,10])
  return ore,nb


def mainloop():
  commands = {
    "ench": Commands.ench,
    "quit": Commands.quit,
    "god": Commands.god,
  }

  indications = {
    "help": Indication.help,
    "credits": Indication.credits,
    "inv": Player.get_inventory,
  }
  
  ressources = {
    "enchantment": {"fortune",}
  }
  print(Indication.intro())
  print(Indication.quotes() + "\n")

  player = Player(input("Choose a name: "))
  
  print(Indication.salutation(player))

  while 1:
    cmd = input("> ").strip()

    if cmd in commands:
      print(commands[cmd](player,ressources))
    elif cmd in indications:
      print(indications[cmd](player))
    else:
      ore, nb = generate_ore(player)
      player.inventory["minerals"][ore][0] += nb

      print(capitalize(ore) + "!")

mainloop()
