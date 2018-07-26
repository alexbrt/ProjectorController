from actions.action import Action
from projectors.christie_projector import ChristieProjector

class RecurrentAction(Action):
	def __init__(self, projector: ChristieProjector, wait_for_response: bool, needs_printing: bool = False):
		super().__init__(projector, wait_for_response, needs_printing)
		self.type = 'recurrent'
