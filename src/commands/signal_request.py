from actions.one_time_action import OneTimeAction
from projectors.christie_projector import ChristieProjector

class SignalRequest(OneTimeAction):
	def __init__(self, projector):
		super().__init__(projector, needs_printing = True)
		self.code = 'sign'

	def exec(self):
		self.response = self.projector.request_signal_group()
		return self.response

	def print_response(self):
		for sign_info in self.response:
			print('\t\t/ {}: {}'.format(sign_info, self.response[sign_info]))
