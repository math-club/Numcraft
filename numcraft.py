#  numcraft.py
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

import random
import time


__version__ = "beta 0.3"
update_title = "Enchantment update"


class Enchant:

  def __init__(self,
               cost: int = 10,
               active: bool = False):
    self.cost = cost
    self.is_active = active

  def activate(self):
    self.is_active = True

  def get_cost(self) -> int:
    return self.cost


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
  return ("Numcraft %s %s" % (__version__, update_title) +
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


def mainloop():
  dimension = 0
  fortune = Enchant(10)

  player_minerals = {
    "diamond": 0,
    "iron": 0,
    "stone": 0
  }


  print(introduction_text())

  while 1:
    cmd = input("> ").strip()

    if cmd == "help":
      print("Numcraft %s %s" % (__version__, update_title))

      print("inv - open your inventory")
      print("ench - list enchantments")
      print("credits - show credits")
    elif cmd == "inv":
      for ore, nb in player_minerals.items():
        print("%s: %s" % (capitalize(ore), nb))
    elif cmd == "ench":
      print("fortune", player_minerals["diamond"],
            "diamonds:", fortune.is_active)

      buying = input("Enchant or EXE to pass: ")

      if buying == "fortune":
        message, value = buy(player_minerals, fortune)
        player_minerals["diamond"] -= value

        print(message)
    elif cmd == "credits":
      print("NumCraft by The ZmaZe")
      print("GNU General Public License 3")
    elif cmd == "quit":
      print("Thank for playing")
      break
    else:
      ore, nb = ore_generation(dimension, fortune)
      player_minerals[ore] += nb

      print("%s !" % capitalize(ore))

      time.sleep(0.1)


mainloop()
