from actions.one_time_action import OneTimeAction
from projectors.projector import Projector

class ConfigurationRequest(OneTimeAction):
	def __init__(self, projector: Projector):
		super().__init__(projector, wait_for_response = True, needs_printing = True)
		self.code = 'conf'

	def exec(self):
		self.response = self.projector.get_configuration_group()
		return self.response

	def print_response(self):
		for conf in self.response:
			print('\t\t/ {}: {}'.format(conf, self.response[conf]))
