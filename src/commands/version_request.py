from actions.one_time_action import OneTimeAction
from projectors.christie_projector import ChristieProjector

class VersionRequest(OneTimeAction):
	def __init__(self, projector: ChristieProjector):
		super().__init__(projector, needs_printing = True)
		self.code = 'vers'

	def exec(self):
		self.response = self.projector.request_version_group()
		return self.response

	def print_response(self):
		for vers_info in self.response:
			print('\t\t/ {}: {}'.format(vers_info, self.response[vers_info]))
