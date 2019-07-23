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

import threading
import time
from actions.action import Action

class ActionManager:
	def __init__(self):
		self.actions = []
		self.responses = {}
		self.background_thread = threading.Thread(target = self.execution_loop)
		self.background_thread.daemon = True
		self.__exit_request = False

	def add_action(self, action: Action):
		self.actions.append(action)

	def remove_action(self, action: Action):
		self.actions.remove(action)

	def clear_reponse(self, action: Action):
		del self.responses[action]

	def execution_loop(self):
		while True:
			if self.__exit_request:
				return

			for action in self.actions:
				self.responses[action] = action.exec()
				if action.type == 'one time':
					self.actions.remove(action)
				elif action.type == 'recurrent':
					pass # Nothing to do, action is recurrent so it stays in the list

			time.sleep(0.1) # Sweep actions every 0.1 seconds
		
	def start(self):
		self.background_thread.start()

	def exit(self):
		self.__exit_request = True

	def __del__(self):
		self.exit()
