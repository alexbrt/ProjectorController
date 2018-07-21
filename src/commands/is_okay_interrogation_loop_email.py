import time

from smtp_service import SMTP_Service
from projector import Projector
from recurrent_action import RecurrentAction

class IsOkayInterrogationLoopEmail(RecurrentAction):
	def __init__(self, projector : Projector, recipients, smtp_service : SMTP_Service = None):
		super().__init__(projector, wait_for_response = True, needs_printing = False)
		if smtp_service:
			self.smtp_service = smtp_service
		self.code = 'is_okay_loop_email'
		self.projector = projector
		self.warning_index = 0
		self.warning_start_time = None
		self.elapsed_time_since_last_warning = 0
		self.sender = smtp_service.user
		self.recipients = recipients

	def exec(self):
		self.projector.update()
		if not self.projector.okay():
			if self.warning_start_time == None:
				self.warning_start_time = time.time()
			self.elapsed_time_since_last_warning = time.time() - self.warning_start_time
			if self.elapsed_time_since_last_warning >= 300 or self.warning_index == 0:
				subject = 'VIDEOPROJECTOR \'{}\' (IP: {}) WARNING #{}'.format(self.projector.name, self.projector.IP[-3:], self.warning_index)
				message = 'Projector {} warning:\n\n'.format(self.projector.IP[-3:])
				# Gather info
				for sensor_ID in self.projector.status.temperatures:
					temperature_warning = 'Videoprojector \'{}\' {}: {} (max acceptable: {}, diff: {})'
					if self.projector.status.temperatures[sensor_ID] >= self.projector.temperature_thresholds[sensor_ID]:
						message += temperature_warning.format(self.projector.name, self.projector.temperature_dictionary[sensor_ID], self.projector.status.temperatures[sensor_ID], self.projector.temperature_thresholds[sensor_ID], self.projector.status.temperatures[sensor_ID] - self.projector.temperature_thresholds[sensor_ID])
						message += '\n'
				self.smtp_service.sendmail(self.sender, self.recipients, subject, message)
				self.warning_index += 1
				self.elapsed_time_since_last_warning = 0
