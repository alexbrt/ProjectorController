#	Copyright (C) 2019 Alexandru-Liviu Bratosin

#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.

#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#	GNU General Public License for more details.

#	You should have received a copy of the GNU General Public License
#	along with this program. If not, see <https://www.gnu.org/licenses/>.

import re

from networking.mysocket import MySocket

class Projector:
	def __init__(self, name : str, IP : str, PORT : str):
		self.name = name
		self.IP = IP
		self.last_IP_digits = IP.split('.')[-1]
		self.PORT = PORT
		self.socket = MySocket()

	def connect(self):
		pass

	def send_command(self, cmd : str):
		pass
