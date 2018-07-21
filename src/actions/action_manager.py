import threading
import time
from action import Action

class ActionManager:
	def __init__(self):
		self.actions = []
		self.responses = {}
		self.background_thread = threading.Thread(target = self.execution_loop)
		self.background_thread.daemon = True

	def add_action(self, action: Action):
		self.actions.append(action)

	def remove_action(self, action: Action):
		self.actions.remove(action)

	def clear_reponse(self, action: Action):
		del self.responses[action]

	def execution_loop(self):
		while True:
			for action in self.actions:
				response = action.exec()
				if action.wait_for_response:
					self.responses[action] = response
				if action.type == 'one time':
					self.actions.remove(action)
				elif action.type == 'recurrent':
					pass # Nothing to do, action is recurrent so it stays in the list
		
	def start(self):
		self.background_thread.start()
