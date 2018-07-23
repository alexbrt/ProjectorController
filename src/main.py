import argparse
import shlex

from networking.smtp_service import SMTP_Service
from projectors.projector import Projector
from projectors.projector_roadie4k45 import ProjectorRoadie4K45
from projectors.projector_boxer import ProjectorBoxer
from projectors.projector_jseries import ProjectorJSeries
from projectors.projector_mseries import ProjectorMSeries
from actions.action_manager import ActionManager
from commands.temperature_request import TemperatureRequest
from commands.configuration_request import ConfigurationRequest
from commands.warning_loop_email import WarningLoopEmail
from commands.update_loop_email import UpdateLoopEmail
from commands.command import Command

def main():
	# Init projector details
	projectors = {}
	projector_names = []
	while not projectors:
		number_of_projectors = int(input('Number of projectors: '))
		for i in range(1, number_of_projectors + 1):
			print()
			name = input('Name of projector {}: '.format(i))
			projector_names.append(name)
			family = input('Family of projector {}: '.format(i))
			IP = input('IP of projector {}: '.format(i))
			PORT = int(input('Port of projector {}: '.format(i)))

			if family == 'roadie4k45' or family == 'r':
				projectors[name] = ProjectorRoadie4K45(name, IP, PORT)
			elif family == 'boxer' or family == 'b':
				projectors[name] = ProjectorBoxer(name, IP, PORT)
			elif family == 'jseries' or family == 'j':
				projectors[name] = ProjectorJSeries(name, IP, PORT)
			elif family == 'mseries' or family == 'm':
				projectors[name] = ProjectorMSeries(name, IP, PORT)

			if not projectors[name].connect():
				del projectors[name]
				projector_names.remove(name)
				continue

		if not projectors:
			print()

	# Init argument parser
	parser = argparse.ArgumentParser()
	parser.add_argument('-v', '--videoprojector', nargs = '*', help = 'videoprojector name / identifier')
	parser.add_argument('-c', '--command', help = 'serial command to be sent to videoprojector')
	parser.add_argument('-p', '--predefined', nargs = '*', help = 'predefined command, such as \'temp\', \'conf\', \'temp_loop_email\', or \'warning_loop_email\'')
	# parser.add_argument('-w', '--wait', action = 'store_true', help = 'wait for reponse after sending command?') # No longer needed

	# Init SMTP
	smtp_credentials_1 = open('./smtp_credentials.txt', 'r').read().splitlines()
	smtp_user_1 = smtp_credentials_1[0][len('user = '):]
	smtp_password_1 = smtp_credentials_1[1][len('password = '):]
	smtp_recipients_1 = [recipient.strip() for recipient in smtp_credentials_1[2][len('recipients = '):].split(',')]
	smtp_service_1 = SMTP_Service(smtp_user_1, smtp_password_1, 'smtp.gmail.com')

	# Init background action manager
	action_manager = ActionManager()
	action_manager.start()

	# Main loop
	args = {}
	destination_projectors = []
	while True:
		# Parse arguments
		astr = input('\n$: ')
		if astr == 'exit':
			break
		try:
			args = vars(parser.parse_args(shlex.split(astr)))
		except SystemExit:
			# Trap argparse error message
			continue

		if args['videoprojector'] is None or args['videoprojector'] == []:
			destination_projectors = projector_names
		else:
			if set(args['videoprojector']).issubset(projector_names):
				destination_projectors = args['videoprojector']
			else:
				print('\'{}\' not a videoprojector'.format(list(set(args['videoprojector']) - set(projector_names))))
				continue

		for projector_name in destination_projectors:
			action = None
			if args['predefined']:
				command_code = args['predefined'][0]
				if 'terminate' in args['predefined']: # if the action needs to be terminated
					for act in action_manager.actions: # parse current actions
						if act.code == command_code and act.projector.name in destination_projectors:
							action_manager.remove_action(act)
				else:
					if command_code == 'temp':
						action = TemperatureRequest(projectors[projector_name])
					elif command_code == 'conf':
						action = ConfigurationRequest(projectors[projector_name])
					elif command_code == 'warning_loop_email':
						warning_interval = float(args['predefined'][1])
						action = WarningLoopEmail(projectors[projector_name], warning_interval, smtp_recipients_1, smtp_service_1)
					elif command_code == 'update_loop_email':
						update_interval = float(args['predefined'][1])
						action = UpdateLoopEmail(projectors[projector_name], update_interval, smtp_recipients_1, smtp_service_1)
			elif args['command']:
				is_request = '?' in args['command']
				action = Command(projectors[projector_name], args['command'], is_request, is_request)

			# Add action
			if action != None:
				action_manager.add_action(action)

				# Print actions that require printing, such as requests - this blocks I/O
				if action.needs_printing:
					while True:
						if action in action_manager.responses:
							if not action_manager.responses[action]:
								print('\n\t# Projector \'{}\' (IP: {}) did not respond'.format(projector_name, projectors[projector_name].last_IP_digits))
							else:
								print('\n\t# Projector \'{}\' (IP: {}) sent the following response:'.format(projector_name, projectors[projector_name].last_IP_digits))
								action.print_response()
							action_manager.clear_reponse(action)
							break
	action_manager.exit()

if __name__ == '__main__':
	main()
