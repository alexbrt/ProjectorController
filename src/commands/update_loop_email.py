import time

from networking.smtp_service import SMTP_Service
from projectors.christie_projector import ChristieProjector
from actions.recurrent_action import RecurrentAction

class UpdateLoopEmail(RecurrentAction):
	def __init__(self, projector : ChristieProjector, update_interval, recipients, smtp_service : SMTP_Service = None):
		super().__init__(projector, needs_printing = False)
		if smtp_service:
			self.smtp_service = smtp_service
		self.code = 'update_loop_email'
		self.projector = projector
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
			self.projector.update() # Update projector attributes

			subject = 'PJ{} \'{}\' UPDATE #{} at {} on {}'.format(self.projector.last_IP_digits, self.projector.name, self.update_index, time.strftime('%X'), time.strftime('%x'))
			message = 'PJ{} {} update at {} on {}:\n'.format(self.projector.last_IP_digits, time.strftime('%X'), time.strftime('%x'))
			message += '\n'

			# Gather configuration info
			message += '# Configuration\n'
			for conf in self.projector.status.configuration_group:
				message += '\t{}: {}\n'.format(conf, self.projector.status.configuration_group[conf])
			message += '\n'

			# Gather system info
			message += '# System\n'
			for s in self.projector.status.system_group:
				message += '\t{}: {}\n'.format(s, self.projector.status.system_group[s])
			message += '\n'

			# Gather lamp info
			message += '# Lamps\n'
			for lamp_info in self.projector.status.lamp_group:
				message += '\t{}: {}\n'.format(lamp_info, self.projector.status.lamp_group[lamp_info])
			message += '\n'

			# Gather temperature info
			message += '# Temperatures\n'
			for sensor_name in self.projector.status.temperature_group:
				message += '\t{}: {} °C\n'.format(sensor_name, self.projector.status.temperature_group[sensor_name])
				
			self.smtp_service.sendmail(self.sender, self.recipients, subject, message)
			self.update_index += 1
			self.last_update_start_time = time.time()
