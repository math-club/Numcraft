#    main.py
#
#    Copyright 2021 Nathan Duranel, Timéo Arnouts
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#    MA 02110-1301, USA.
#
#
__version__ = "beta 1"
__author__ = [
    "Nathan Duranel",
    "Timéo Arnouts"
]


import re

import functions as numcraft


game_name = "NumCraft"
update_name = "BETA"


def mainloop():
    commands = {
        "ench": numcraft.Commands.ench,
        "quit": numcraft.Commands.quit,
        "god": numcraft.Commands.god,
        "save": numcraft.Commands.save,
        "movup": numcraft.Commands.move_up,
        "movdwn": numcraft.Commands.move_down,
    }

    indications = {
        "help": numcraft.Indication.help,
        "credits": numcraft.Indication.credits,
        "inv": numcraft.Player.get_inventory,
        "player": numcraft.Indication.player_infos,
        "players": numcraft.Indication.players_list,
    }

    ressources = {
        "enchantment": {"fortune", },
        "y_levels": {"surface": ((20, 80), "surface_ressources", 2),
                     "caves": ((1, 15, 84), "minerals", 1),
                     "mine": ((1, 10, 89), "minerals", 0), },
        "y_levels_list": ("mine",
                          "caves",
                          "surface")
    }

    player_defined = 0

    try:
        open("id_list.numcraft", "r").close()
    except FileNotFoundError:
        open("id_list.numcraft", "w").close()

    print(numcraft.Indication.intro())
    print(numcraft.Indication.quotes() + "\n")

    main_choice = 0
    while not (main_choice == "n" or main_choice == "c"):
        main_choice = input(
            "n: New numcraft.Player c: Charge numcraft.Player [n/c]: ")

    if main_choice == "n":
        while not player_defined:
            try:
                player_name = input("Choose a name: ")
                player_id = numcraft.validate_player(player_name)
                player_defined = 1
            except numcraft.PlayerError as player_error:
                print(player_error.args[0])
        player = numcraft.Player(player_name, player_id)

    elif main_choice == "c":
        print(numcraft.Indication.players_list(None))
        player_id = 0
        file_exist = 0
        while not numcraft.verify_id(player_id) or not file_exist:
            player_id = input("Enter ID ")
            if not numcraft.verify_id(player_id):
                print("Unrecognized ID")
            try:
                open("%s.save.numcraft" % (player_id), "r")
            except FileNotFoundError:
                print("Save file not saved, deleted or bad-named")
            else:
                file_exist = 1
        player = numcraft.read_save(player_id)

    else:
        raise numcraft.MainChoiceError()

    print(numcraft.Indication.salutation(player))

    while 1:
        cmd = input("> ").strip()

        if cmd in commands:
            print(commands[cmd](player, ressources))
        elif cmd in indications:
            print(indications[cmd](player))
        else:
            ore, nb, category = numcraft.generate_ore(player, ressources)
            player.inventory[category][ore][0] += nb

            print(ore.capitalize() + "!")


mainloop()
