from actions.one_time_action import OneTimeAction
from projectors.christie_projector import ChristieProjector

class SystemRequest(OneTimeAction):
	def __init__(self, projector: ChristieProjector):
		super().__init__(projector, needs_printing = True)
		self.code = 'sys'

	def exec(self):
		self.response = self.projector.request_system_group()
		return self.response

	def print_response(self):
		for system_info in self.response:
			print('\t\t/ {}: {}'.format(system_info, self.response[system_info]))
