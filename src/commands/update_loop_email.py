import time

from networking.smtp_service import SMTP_Service
from projectors.projector import Projector
from actions.recurrent_action import RecurrentAction

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
			subject = 'PJ{} \'{}\' UPDATE #{}'.format(self.projector.last_IP_digits, self.projector.name, self.update_index)
			message = 'PJ{} {} update at {} on {}:\n'.format(self.projector.last_IP_digits, self.projector.family, time.strftime('%X'), time.strftime('%x'))
			message += '\n'
			# Gather configuration info
			message += '# Configuration\n'
			for conf in self.projector.configuration:
				message += '\t{}: {}\n'.format(conf, self.projector.configuration.values[conf])
			message += '\n'
			# Gather temperature info
			message += '# Temperatures\n'
			for sensor_name in self.projector.status.temperatures:
				temperature_update = '\t{}: current {} / warning {}\n'
				message += temperature_update.format(sensor_name, self.projector.status.temperatures[sensor_name], self.projector.temperature_thresholds[sensor_name])
			self.smtp_service.sendmail(self.sender, self.recipients, subject, message)
			self.update_index += 1
			self.last_update_start_time = time.time()
