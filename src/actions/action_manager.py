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
