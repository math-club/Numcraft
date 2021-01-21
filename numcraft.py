#NumCraft 0.3 beta

#Copyright 2021 The ZmaZe

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <https://www.gnu.org/licenses/>.



from random import randint
from numcraft_class import*
import time

def clicker():
  global diamond,iron,stone
  randclick=randint(1,100)

  if dimension==0:
    if randclick<=1:
      diamond+=1*(1+fortune.get_active())
      print("Diamond!")

    elif randclick<=11 and randclick>1:
      iron+=2*(1+fortune.get_active())
      print("Iron!")

    else:
      stone+=1
      print("Mining")


def buy(ench):
  global diamond
  if ench.get_active():
    print("Sorry, enchantment already owned")
  
  else:
    if diamond<ench.cost:
      print("Sorry, not enough diamonds")
    
    else:
      ench.activate()
      diamond-=ench.cost
      print("Succesfully applied fortune")


def numcraft_play():
  global diamond,iron,stone
  diamond,iron,stone=0,0,0
  
  global dimension
  dimension=0
  
  global fortune
  fortune=Enchant(10)
  
  while 1:
    click=input("Click EXE or help: ")

    if click=="help":
      print("Numcraft beta 0.3")
      print("Enchanting Update")

      print("inv - open your inventory")
      print("ench - list enchantments")
      print("credits - show credits")

    elif click=="inv":
      print("Stone: ",stone)
      print("Diamonds: ",diamond)
      print("Iron: ",iron)

    elif click=="credits":
      print("NumCraft by The ZmaZe")
      print("GNU General Public License 3")

    elif click=="ench":
      print("fortune",diamond,"diamonds:",fortune.get_active())
      buying=input("Enchant or EXE to pass: ")

      if buying=="fortune":
        buy(fortune)

    else:
      clicker()
      time.sleep(0.1)
