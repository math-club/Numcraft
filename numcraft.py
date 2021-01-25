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


class Player:

  def __init__(self,
               name: str):
    self.name = name
    self.current_dimension = 0

    self.inventory = {
      "minerals": {"diamond": 0,
                   "iron": 0,
                   "stone": 0}
    }
    self.enchantments = []

  def get_inventory(self) -> str:
    return "\n".join("%s: %s" % (capitalize(ore), nb)
                     for ore, nb in self.inventory["minerals"].items())


  def get_enchantments(self) -> list:
    return self.enchantments

  def get_name(self) -> str:
    return self.name


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

  def quit(player) -> str:
    """leave game"""
    return "Thanks for playing"


def generate_ore(player,enchantment):
  if player.current_dimension == 0:
    ore = weight_choice(list(
      ore for ore,x in player.inventory["minerals"].items()),[1,10,89])
    nb = 1
    if enchantment["fortune"] in player.get_enchantments: nb = nb*2
  return ore,nb


def buy(ores, ench):
  if ench.is_active:
    return "Sorry, enchantment already owned", 0
  else:
    if ores["diamond"] < ench.cost:
      return "Sorry, not enough diamonds", 0
    else:
      ench.activate()

      return "Succesfully applied fortune", ench.cost


def mainloop():
  commands = {
    "inv": Player.get_inventory,
    "ench": Player.get_enchantments
  }

  indications = {
    "help": Indication.help,
    "credits": Indication.credits,
    "quit": Indication.quit,
  }
  
  enchantment = {
    "fortune": 10
  }

  print(Indication.intro())
  print(Indication.quotes() + "\n")

  gamer = Player(input("Choose a name: "))
  
  print(Indication.salutation(gamer))

  while 1:
    cmd = input("> ").strip()

    if cmd in commands:
      print(commands[cmd](gamer))
    elif cmd in indications:
      print(indications[cmd](gamer))
    else:
      ore, nb = generate_ore(gamer,enchantment)
      gamer.inventory["minerals"][ore] += nb

      print(capitalize(ore) + "!")

mainloop()
