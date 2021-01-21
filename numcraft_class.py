#This file is part of NumCraft.

#NumCraft is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#NumCraft is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with NumCraft.  If not, see <https://www.gnu.org/licenses/>.



class Enchant:
  def __init__(self,cost=10,active=False):
    self.cost=cost
    self.active=active

  def get_active(self):
    return self.active

  def get_cost(self):
    return self.cost

  def activate(self):
    self.active=True


