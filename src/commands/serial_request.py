from actions.one_time_action import OneTimeAction
from projectors.christie_projector import ChristieProjector

class SerialRequest(OneTimeAction):
	def __init__(self, projector: ChristieProjector):
		super().__init__(projector, needs_printing = True)
		self.code = 'serial'

	def exec(self):
		self.response = self.projector.request_serial_group()
		return self.response

	def print_response(self):
		for serial_info in self.response:
			print('\t\t/ {}: {}'.format(serial_info, self.response[serial_info]))
