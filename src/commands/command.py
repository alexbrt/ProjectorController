import re

from actions.one_time_action import OneTimeAction
from projectors.christie_projector import ChristieProjector

class Command(OneTimeAction):
	def __init__(self, projector: ChristieProjector, cmd: str, needs_printing: bool):
		super().__init__(projector, needs_printing)
		self.projector = projector
		self.cmd = cmd
		self.code = 'command'
	
	def exec(self):
		self.response = self.projector.send_command(self.cmd)
		return self.response

	def print_response(self):
		formatted = ''
		start_index = 0
		occ = re.finditer(r'(?<!\\)\)', self.response)
		for m in occ:
			if start_index != 0:
				formatted += '\n'
			formatted += '\t\t/ ' + self.response[start_index:m.end()]
			start_index = m.end()
		else:
			if not formatted:
				formatted = '\t\t/ ' + self.response
		print(formatted)
