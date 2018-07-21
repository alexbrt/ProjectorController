from one_time_action import OneTimeAction
from projector import Projector

class Command(OneTimeAction):
	def __init__(self, projector: Projector, cmd: str, wait_for_response: bool, needs_printing: bool):
		super().__init__(projector, wait_for_response, needs_printing)
		self.projector = projector
		self.cmd = cmd
		self.wait_for_response = wait_for_response
		self.code = 'command'
	
	def exec(self):
		self.response = self.projector.send_command(self.cmd, self.wait_for_response)
		return self.response

	def print_response(self):
		print('\t\t/ {}'.format(self.response))
