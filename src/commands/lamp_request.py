from actions.one_time_action import OneTimeAction
from projectors.projector import Projector

class LampRequest(OneTimeAction):
	def __init__(self, projector: Projector):
		super().__init__(projector, wait_for_response = True, needs_printing = True)
		self.code = 'lamp'

	def exec(self):
		self.response = self.projector.request_lamp_group()
		return self.response

	def print_response(self):
		for lamp_info in self.response:
			print('\t\t/ {}: {}'.format(lamp_info, self.response[lamp_info]))
