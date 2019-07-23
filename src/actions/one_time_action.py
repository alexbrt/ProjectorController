from actions.action import Action
from projectors.christie_projector import ChristieProjector

class OneTimeAction(Action):
	def __init__(self, projector: ChristieProjector, needs_printing: bool = False):
		super().__init__(projector, needs_printing)
		self.type = 'one time'
