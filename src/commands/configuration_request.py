from actions.one_time_action import OneTimeAction
from projectors.christie_projector import ChristieProjector

class ConfigurationRequest(OneTimeAction):
	def __init__(self, projector: ChristieProjector):
		super().__init__(projector, needs_printing = True)
		self.code = 'conf'

	def exec(self):
		self.response = self.projector.request_configuration_group()
		return self.response

	def print_response(self):
		for conf_info in self.response:
			print('\t\t/ {}: {}'.format(conf_info, self.response[conf_info]))
