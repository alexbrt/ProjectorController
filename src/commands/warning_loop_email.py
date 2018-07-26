import time

from networking.smtp_service import SMTP_Service
from projectors.christie_projector import ChristieProjector
from actions.recurrent_action import RecurrentAction

class WarningLoopEmail(RecurrentAction):
	def __init__(self, projector : ChristieProjector, warning_interval, recipients, smtp_service : SMTP_Service = None):
		super().__init__(projector, wait_for_response = True, needs_printing = False)
		if smtp_service:
			self.smtp_service = smtp_service
		self.code = 'warning_loop_email'
		self.projector = projector
		self.warning_index = 0
		self.warning_interval = warning_interval
		self.last_warning_start_time = None
		self.elapsed_time_since_last_warning = 0
		self.sender = smtp_service.user
		self.recipients = recipients

	def exec(self):
		self.projector.update()
		if not self.projector.okay():
			if self.last_warning_start_time == None:
				self.last_warning_start_time = time.time()

			self.elapsed_time_since_last_warning = time.time() - self.last_warning_start_time
			if self.elapsed_time_since_last_warning >= self.warning_interval or self.warning_index == 0:
				subject = 'PJ{} \'{}\' WARNING #{}'.format(self.projector.last_IP_digits, self.projector.name, self.warning_index)
				message = 'PJ{} {} warning at {} on {}:\n\n'.format(self.projector.last_IP_digits, self.projector.family, time.strftime('%X'), time.strftime('%x'))
				# Gather info
				for sensor_name in self.projector.status.temperature_group:
					temperature_warning = '{}: {} (max acceptable: {}, diff: {})'
					if self.projector.status.temperature_group[sensor_name] >= self.projector.temperature_thresholds[sensor_name]:
						message += temperature_warning.format(sensor_name, self.projector.status.temperature_group[sensor_name], self.projector.temperature_thresholds[sensor_name], self.projector.status.temperature_group[sensor_name] - self.projector.temperature_thresholds[sensor_name])
						message += '\n'
				self.smtp_service.sendmail(self.sender, self.recipients, subject, message)
				self.warning_index += 1
				self.last_warning_start_time = time.time()
