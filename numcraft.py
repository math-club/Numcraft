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
__version__ = "beta 0.3"
__author__ = [
  "Nathan Duranel",
  "Timéo Arnouts"
]


import random


game_name = "Numcraft"
update_name = "Code update"


class Enchantment:

  def __init__(self,
               cost: int = 10,
               active: bool = False):
    self.cost = cost
    self.is_active = active

  def activate(self):
    self.is_active = True


class Player:

  def __init__(self,
               name: str):
    self.name = name



def capitalize(string: str) -> str:
  return string[0].upper() + string[1:]


def generate_ore(dimension: int,
                 fortune):
  randclick = random.randint(1, 100)

  if dimension == 0:
    if randclick <= 1:
      return "diamond", 1*(1 + fortune.is_active)
    elif 1 < randclick <= 11:
      return "iron", 2*(1 + fortune.is_active)
    else:
      return "stone", 1


class Indication:

  def intro() -> str:
    return ("%s %s %s. " % (game_name,__version__, update_name) +
            'Type "help" or "credits" for more information.')

  def help() -> str:
    return ("%s %s %s\n" % (game_name,__version__, update_name) +
            "inv - open your inventory\n"
            "ench - list enchantments\n"
            "credits - show credits\n"
            "quit - leave game")

  def credits() -> str:
    return "Authors : %s" % ", ".join(__author__)

  def quit() -> str:
    return "Thanks for playing"


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
  dimension = 0
  fortune = Enchantment(10)

  player_minerals = {
    "diamond": 0,
    "iron": 0,
    "stone": 0
  }

  commands = {
    "intro": Indication.intro,
    "help": Indication.help,
    "credits": Indication.credits,
    "quit": Indication.quit,
    "inv": Player.inventory,
    "ench": Player.enchantments
  }

  print(Indication.intro())

  while 1:
    cmd = input("> ").strip()

    if cmd in commands:
      commands[cmd]()
    else:
      ore, nb = generate_ore(dimension, fortune)
      player_minerals[ore] += nb

      print("%s !" % capitalize(ore))

    # ~ elif cmd == "inv":
      # ~ for ore, nb in player_minerals.items():
        # ~ print("%s: %s" % (capitalize(ore), nb))
    # ~ elif cmd == "ench":
      # ~ print("fortune for", fortune.cost,
            # ~ "diamonds:", fortune.is_active)

      # ~ buying = input("Enchant or EXE to pass: ")

      # ~ if buying == "fortune":
        # ~ message, value = buy(player_minerals, fortune)
        # ~ player_minerals["diamond"] -= value

        # ~ print(message)


mainloop()
