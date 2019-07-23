from actions.one_time_action import OneTimeAction
from projectors.christie_projector import ChristieProjector

class CoolingRequest(OneTimeAction):
	def __init__(self, projector: ChristieProjector):
		super().__init__(projector, needs_printing = True)
		self.code = 'cool'

	def exec(self):
		self.response = self.projector.request_cooling_group()
		return self.response

	def print_response(self):
		for cool_info in self.response:
			print('\t\t/ {}: {}'.format(cool_info, self.response[cool_info]))
