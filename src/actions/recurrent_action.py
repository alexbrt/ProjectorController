from action import Action
from projector import Projector

class RecurrentAction(Action):
	def __init__(self, projector: Projector, wait_for_response: bool, needs_printing: bool = False):
		super().__init__(projector, wait_for_response, needs_printing)
		self.type = 'recurrent'
