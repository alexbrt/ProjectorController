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

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class SMTP_Service:
	def __init__(self, user : str, password : str, server : str):
		# Init SMTP connection
		self.user = user
		self.password = password
		self.server = server

	def sendmail(self, sender : str, recipients : [str], subject : str, message : str):
		# Prepare email
		mail = MIMEMultipart()
		mail['From'] = sender
		mail['To'] = ', '.join(recipients)
		mail['Subject'] = subject
		mail.attach(MIMEText(message, 'plain'))
		# Send email
		smtp_server = smtplib.SMTP_SSL(self.server, 465)
		smtp_server.login(self.user, self.password)
		smtp_server.sendmail(sender, recipients, mail.as_string())
		smtp_server.quit()
