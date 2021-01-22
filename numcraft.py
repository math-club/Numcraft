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
__license__ = "GNU General Public License 3"


import random


game_name = "Numcraft"
update_title = "Code update"
quit_message = "Thanks for playing"

work_team = "BG de NSI"
game_designers = [
  "Paul Boëté",
  "Nathan Duranel",
  "Timéo Arnouts"
]


class Enchantment:

  def __init__(self,
               cost: int = 10,
               active: bool = False):
    self.cost = cost
    self.is_active = active

  def activate(self):
    self.is_active = True


def capitalize(string: str) -> str:
  return string[0].upper() + string[1:]


def ore_generation(dimension: int,
                   fortune):
  randclick = random.randint(1, 100)

  if dimension == 0:
    if randclick <= 1:
      return "diamond", 1*(1 + fortune.is_active)
    elif 1 < randclick <= 11:
      return "iron", 2*(1 + fortune.is_active)
    else:
      return "stone", 1


def introduction_text() -> str:
  return ("%s %s %s. " % (game_name,__version__, update_title) +
          'Type "help" or "credits" for more information.')


def buy(ores, ench):
  if ench.is_active:
    return "Sorry, enchantment already owned", 0
  else:
    if ores["diamond"] < ench.cost:
      return "Sorry, not enough diamonds", 0
    else:
      ench.activate()
      return "Succesfully applied fortune", ench.cost


def cmd_help():
  return str("%s %s %s\n" % (game_name,__version__, update_title) +
    "inv - open your inventory\n" +
    "ench - list enchantments\n" +
    "credits - show credits\n" +
    "quit - leave game")

def cmd_credits():
  pass

def cmd_quit():
  

def cmd_inv():
  pass

def cmd_enchant():
  pass


def mainloop():
  dimension = 0
  fortune = Enchantment(10)

  player_minerals = {
    "diamond": 0,
    "iron": 0,
    "stone": 0
  }

  cmds = {
    "help": cmd_help(),
    "credits": cmd_credits(),
    "quit": cmd_quit(),
    "inv": cmd_inv(),
    "ench": cmd_enchant()
  }

  print(introduction_text())

  while 1:
    cmd = input("> ").strip()

    print(cmds[cmd])
    # ~ if cmd == "help":
      # ~ print("%s %s %s" % (game_name,__version__, update_title))

      # ~ print("inv - open your inventory")
      # ~ print("ench - list enchantments")
      # ~ print("credits - show credits")
      # ~ print("quit - leave game")
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
    # ~ elif cmd == "credits":
      # ~ print("%s by %s" % (game_name,work_team))
      # ~ print("Devs:")
      # ~ for name in __author__: print(" - %s" % (name))
      # ~ print("Game Designers:")
      # ~ for name in game_designers: print(" - %s" % (name))
      # ~ print(__license__)
    # ~ elif cmd == "quit":
      # ~ print(quit_message)
      # ~ break
    # ~ else:
      # ~ ore, nb = ore_generation(dimension, fortune)
      # ~ player_minerals[ore] += nb

      # ~ print("%s !" % capitalize(ore))


mainloop()
