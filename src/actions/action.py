from projectors.projector import Projector

class Action:
	def __init__(self, projector: Projector, wait_for_response: bool, needs_printing: bool = False):
		self.projector = projector
		self.wait_for_response = wait_for_response
		self.response = None
		self.needs_printing = needs_printing
		self.code = ''

	def exec(self):
		return None

	def print_response():
		pass
