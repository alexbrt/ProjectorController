import time

from smtp_service import SMTP_Service
from projector import Projector
from recurrent_action import RecurrentAction

class UpdateLoopEmail(RecurrentAction):
	def __init__(self, projector : Projector, update_interval, recipients, smtp_service : SMTP_Service = None):
		super().__init__(projector, wait_for_response = True, needs_printing = False)
		if smtp_service:
			self.smtp_service = smtp_service
		self.code = 'update_loop_email'
		self.projector = projector
		self.update_index = 0
		self.update_interval = update_interval
		self.last_update_start_time = None
		self.elapsed_time_since_last_update = 0
		self.sender = smtp_service.user
		self.recipients = recipients

	def exec(self):
		if self.last_update_start_time == None:
			self.last_update_start_time = time.time()

		self.elapsed_time_since_last_update = time.time() - self.last_update_start_time
		if self.elapsed_time_since_last_update >= self.update_interval or self.update_index == 0: # In seconds
			self.projector.update()
			subject = 'VIDEOPROJECTOR \'{}\' (IP: {}) UPDATE #{}'.format(self.projector.name, self.projector.IP[-3:], self.update_index)
			message = 'Projector {} update:\n\n'.format(self.projector.IP[-3:])
			# Gather info
			for sensor_ID in self.projector.status.temperatures:
				temperature_update = 'Videoprojector \'{}\' {}: {}'
				message += temperature_update.format(self.projector.name, self.projector.temperature_dictionary[sensor_ID], self.projector.status.temperatures[sensor_ID])
				message += '\n'
			self.smtp_service.sendmail(self.sender, self.recipients, subject, message)
			self.update_index += 1
			self.last_update_start_time = time.time()
