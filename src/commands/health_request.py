from actions.one_time_action import OneTimeAction
from projectors.christie_projector import ChristieProjector

class HealthRequest(OneTimeAction):
	def __init__(self, projector):
		super().__init__(projector, needs_printing = True)
		self.code = 'health'

	def exec(self):
		self.response = self.projector.request_health_group()
		return self.response

	def print_response(self):
		for health_info in self.response:
			print('\t\t/ {}: {}'.format(health_info, self.response[health_info]))
