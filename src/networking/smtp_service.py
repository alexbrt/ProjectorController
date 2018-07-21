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
