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

class ChristieProjectorStatus:
	def __init__(self):
		self.configuration_group = {}
		self.system_group = {}
		self.signal_group = {}
		self.lamp_group = {}
		self.version_group = {}
		self.temperature_group = {}
		self.cooling_group = {}
		self.health_group = {}
		self.serial_group = {}
