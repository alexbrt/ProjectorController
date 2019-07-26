#	Copyright (C) 2019 Alexandru-Liviu Bratosin

#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.

#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#	GNU General Public License for more details.

#	You should have received a copy of the GNU General Public License
#	along with this program. If not, see <https://www.gnu.org/licenses/>.

import argparse
import shlex

from networking.smtp_service import SMTP_Service
from projectors.christie_projector import ChristieProjector
from actions.action_manager import ActionManager
from commands.temperature_request import TemperatureRequest
from commands.configuration_request import ConfigurationRequest
from commands.system_request import SystemRequest
from commands.version_request import VersionRequest
from commands.signal_request import SignalRequest
from commands.cooling_request import CoolingRequest
from commands.health_request import HealthRequest
from commands.serial_request import SerialRequest
from commands.lamp_request import LampRequest
from commands.update_loop_email import UpdateLoopEmail
from commands.command import Command

def main():
	# Init SMTP
	smtp_server = None
	smtp_user = None
	smtp_password = None
	smtp_recipients = None
	smtp_service = None
	use_smtp = input('Use SMTP? (y/n): ')
	if use_smtp == 'y':
		smtp_server = input('\t / SMTP Server: ')
		smtp_user = input('\t / User: ')
		smtp_password = input('\t / Password: ')
		smtp_recipients = [recipient.strip() for recipient in input('\t / Recipients: ').split(',')]
		smtp_service = SMTP_Service(smtp_user, smtp_password, smtp_server)
		print()

	# Init projector details
	IP_class = input('IP class (leave blank if different among projectors): ')
	default_port = input('Default port (leave blank if different among projectors): ')
	print()
	if IP_class:
		IP_class += '.'
	if default_port:
		default_port = int(default_port)

	projectors = {}
	projector_names = []
	while not projectors:
		number_of_projectors = int(input('Number of projectors: '))
		for i in range(1, number_of_projectors + 1):
			print()
			name = input('Name of projector {}: '.format(i))
			projector_names.append(name)
			IP = IP_class + input('IP of projector {}: {}'.format(i, IP_class))
			if not default_port:
				PORT = int(input('Port of projector {}: '.format(i)))
			else:
				PORT = default_port
			# Init projector
			projectors[name] = ChristieProjector(name, IP, PORT)

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
	parser.add_argument('-p', '--predefined', nargs = '*', help = 'predefined command, such as \'temp\', \'conf\', \'sys\', \'lamp\', \'cool\', \'seri\', \'sign\', \'health\', \'vers\', or \'update_loop_email <seconds>\'')

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
					elif command_code == 'sys':
						action = SystemRequest(projectors[projector_name])
					elif command_code == 'vers':
						action = VersionRequest(projectors[projector_name])
					elif command_code == 'sign':
						action = SignalRequest(projectors[projector_name])
					elif command_code == 'cool':
						action = CoolingRequest(projectors[projector_name])
					elif command_code == 'health':
						action = HealthRequest(projectors[projector_name])
					elif command_code == 'serial':
						action = SerialRequest(projectors[projector_name])
					elif command_code == 'lamp':
						action = LampRequest(projectors[projector_name])
					elif command_code == 'update_loop_email' and use_smtp:
						update_interval = float(args['predefined'][1])
						action = UpdateLoopEmail(projectors[projector_name], update_interval, smtp_recipients, smtp_service)
			elif args['command']:
				is_request = '?' in args['command']
				action = Command(projectors[projector_name], args['command'], is_request)

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
