import argparse
import shlex

from smtp_service import SMTP_Service
from projector import Projector
from projector_roadie4k45 import ProjectorRoadie4k45
from action_manager import ActionManager
from temperature_request import TemperatureRequest
from is_okay_interrogation_loop_email import IsOkayInterrogationLoopEmail
from command import Command

def main():
	# Init projector details
	projectors = {}
	projector_names = []
	while not projectors:
		number_of_projectors = int(input('Number of projectors: '))
		for i in range(number_of_projectors):
			print()
			name = input('Name of projector {}: '.format(i))
			projector_names.append(name)
			family = input('Family of projector {}: '.format(i))
			IP = input('IP of projector {}: '.format(i))
			PORT = int(input('Port of projector {}: '.format(i)))
			if family == 'roadie4k45':
				projectors[name] = ProjectorRoadie4k45(name, IP, PORT)
			if not projectors[name].connect():
				del projectors[name]
				projector_names.remove(name)
		if not projectors:
			print()

	# Init argument parser
	parser = argparse.ArgumentParser()
	parser.add_argument('-v', '--videoprojector', nargs = '*', help = 'videoprojector name / identifier')
	parser.add_argument('-c', '--command', help = 'command to be sent to videoprojector')
	parser.add_argument('-p', '--predefined', nargs = '*', help = 'predefined command, such as \'temp\', \'temp_loop_email\'')
	parser.add_argument('-w', '--wait', action = 'store_true', help = 'wait for reponse after sending command?')

	# Init SMTP
	smtp_credentials_1 = open('smtp_credentials.txt', 'r').read().splitlines()
	smtp_user_1 = smtp_credentials_1[0][len('user = '):]
	smtp_password_1 = smtp_credentials_1[1][len('password = '):]
	smtp_recipients_1 = [recipient.strip() for recipient in smtp_credentials_1[2][len('recipients = '):].split(",")]
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
			quit()
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
					#action_manager.remove_action(recurrent_actions[projector_name][args['predefined'][0]])
					#del recurrent_actions[projector_name][args['predefined'][0]]
				else:
					if command_code == 'temp':
						action = TemperatureRequest(projectors[projector_name])
					elif command_code == 'is_okay_loop_email':
						action = IsOkayInterrogationLoopEmail(projectors[projector_name], smtp_recipients_1, smtp_service_1)
			elif args['command']:
				action = Command(projectors[projector_name], args['command'], args['wait'], args['wait'])

			# Add action
			if action != None:
				action_manager.add_action(action)

				# Print actions that require printing, such as requests - this blocks I/O
				if action.needs_printing:
					while True:
						if action in action_manager.responses:
							if not action_manager.responses[action]:
								print('\n\t# Projector \'{}\' (IP: {}) did not respond'.format(projector_name, projectors[projector_name].IP[-3:]))
							else:
								print('\n\t# Projector \'{}\' (IP: {}) sent following response:'.format(projector_name, projectors[projector_name].IP[-3:]))
								action.print_response()
							action_manager.clear_reponse(action)
							break

if __name__ == '__main__':
	main()

