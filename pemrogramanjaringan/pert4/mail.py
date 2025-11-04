import smtplib
from email.message import EmailMessage

smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_username = 'rthnissi@gmail.com'
smtp_password = 'ipfr rzyt nwbp icwm' #google app passwords

msg = EmailMessage()
msg['From'] = 'rthnissi@gmail.com'
msg['To'] = 'ing.group3@gmail.com'
msg['Subject'] = 'Test Email'
msg.set_content('This is a test')

with smtplib.SMTP(smtp_server, smtp_port) as smtp:
    smtp.starttls()
    smtp.login(smtp_username, smtp_password)
    smtp.send_message(msg)