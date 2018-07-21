from mysocket import MySocket
from projector_status import ProjectorStatus

class Projector:
	def __init__(self, name : str, IP : str, PORT : str):
		self.name = name
		self.IP = IP
		self.PORT = PORT
		self.socket = MySocket()
		self.status = ProjectorStatus()

	def connect(self):
		try:
			self.socket.connect(self.IP, self.PORT)
		except:
			print('ERROR: Could not connect to projector \'{}\''.format(self.name))
			return False
		return True

	def send_command(self, cmd : str, wait_for_response : bool = False):
		self.socket.send(cmd.encode())
		if wait_for_response:
			response = self.socket.receive().decode()
			if response:
				return response
		return None

	def get_status(self):
		return self.status
	
	def update(self):
		#raise NotImplementedError('Subclass must implement abstract method')
		return None

	def is_okay(self):
		#raise NotImplementedError('Subclass must implement abstract method')
		return None

	def request_temperatures(self):
		#raise NotImplementedError('Subclass must implement abstract method')
		return {}
