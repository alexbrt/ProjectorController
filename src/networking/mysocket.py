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

import socket
import time
import struct
import string

class MySocket:
	def __init__(self, sock = None):
		if sock is None:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		else:
			self.sock = sock

	def connect(self, host, port):
		self.IP = host
		self.PORT = port
		self.sock.connect((host, port))

	def send(self, message):
		totalsent = 0
		while totalsent < len(message):
			sent = self.sock.send(message[totalsent:])
			if sent == 0:
				raise RuntimeError('Socket connection broken')
			totalsent = totalsent + sent

	def receive(self, end):
		# Total data partwise in an array
		total_data = []
		data = ''

		while True:
			data = self.sock.recv(1024)
			if end in data:
				total_data.append(data[:data.find(end)])
				break
			total_data.append(data)

		return b''.join(total_data)

	def __del__(self):
		self.sock.close()
