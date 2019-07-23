from projectors.christie_projector import ChristieProjector

class Action:
	def __init__(self, projector: ChristieProjector, needs_printing: bool = False):
		self.projector = projector
		self.response = None
		self.needs_printing = needs_printing
		self.code = ''

	def exec(self):
		return None

	def print_response():
		pass
