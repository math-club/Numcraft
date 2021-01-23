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
splash_text = [
  "Also try Minecraft!"
  "Coding UTF-8!"
  "GG!"
  "The answer is 42"
  "Also try Archess_btw!"
]

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
    self.current_dimension = 0

    self.inventory = {
      "minerals": {"diamond": 0,
                   "iron": 0,
                   "stone": 0}
    }
    self.enchantments = []

  def get_inventory(self) -> dict:
    return self.inventory

  def get_enchantments(self) -> list:
    return self.enchantments

  def get_name(self) -> str:
    return self.name


class Indication:

  def intro() -> str:
    return ("%s %s %s. \n" % (game_name,__version__, update_name) +
            'Type "help" or "credits" for more information.')

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
  
  def inv(player) ->str:
    """show inventory"""
    return ("%s's Inventory" % (player.get_name))

  def quotes():
    return random.choice(splash_text)
    


def capitalize(string: str) -> str:
  return string[0].upper() + string[1:]


def weight_choice(choices_list: list,weight: list):
  if len(choices_list)==len(weight):
    weighted=[]
    for i in range(len(choices_list)):
      weighted += list(choices_list[i] for x in range(weight[i]))
    return choice(weighted)
  else: raise ValueError("In Function: weight_choices() - len(choices_list) and len(weight) must be equals ")


def generate_ore(player):
  randclick = random.randint(1, 100)

  if player.current_dimension == 0:
    if randclick <= 1:
      return "diamond", 1*(1 + ("fortune" in player.enchantments))
    elif 1 < randclick <= 11:
      return "iron", 2*(1 + ("fortune" in player.enchantments))
    else:
      return "stone", 1


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
  fortune = Enchantment(10)

  loop_index = 1

  commands = {
    "inv": Player.get_inventory,
    "ench": Player.get_enchantments
  }

  indications = {
    "intro": Indication.intro,
    "quote": Indication.quotes,
    "help": Indication.help,
    "credits": Indication.credits,
    "quit": Indication.quit,
    "inv": Indication.inv
  }

  print(Indication.intro())
  print(Indication.quotes())

  while 1:
    
    if loop_index == 1:
      gamer = Player(input("Choose a name: "))

    cmd = input("> ").strip()

    if cmd in commands:
      commands[cmd](gamer)
    if cmd in indications:
      print(indications[cmd](gamer))
    else:
      ore, nb = generate_ore(gamer)
      gamer.inventory["minerals"][ore] += nb

      print("%s !" % capitalize(ore))
    loop_index += 1
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
