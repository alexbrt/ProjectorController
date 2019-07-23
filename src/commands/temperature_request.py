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

from actions.one_time_action import OneTimeAction
from projectors.christie_projector import ChristieProjector

class TemperatureRequest(OneTimeAction):
	def __init__(self, projector: ChristieProjector):
		super().__init__(projector, needs_printing = True)
		self.code = 'temp'

	def exec(self):
		self.response = self.projector.request_temperature_group()
		return self.response

	def print_response(self):
		for sensor_name in self.response:
			print('\t\t/ {}: {} °C'.format(sensor_name, self.response[sensor_name]))
