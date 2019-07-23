from actions.action import Action
from projectors.christie_projector import ChristieProjector

class RecurrentAction(Action):
	def __init__(self, projector: ChristieProjector, needs_printing: bool = False):
		super().__init__(projector, needs_printing)
		self.type = 'recurrent'
