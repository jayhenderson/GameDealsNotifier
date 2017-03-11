import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import configparser

SETTINGS = configparser.ConfigParser()
SETTINGS.read('email.ini')


def create_server():
    user = SETTINGS.get('SenderEmail', 'Email')
    password = SETTINGS.get('SenderEmail', 'Password')
    smtp_server = smtplib.SMTP_SSL(SETTINGS.get('SenderEmail', 'Server'))
    smtp_server.login(user, password)
    return smtp_server


def create_email_string(subject, body):
    msg = MIMEMultipart()
    msg['From'] = SETTINGS.get('SenderEmail', 'Name') + " <" + SETTINGS.get('SenderEmail', 'Email') + ">"
    msg['To'] = SETTINGS.get('DestinationEmail', 'Email')
    msg['Subject'] = subject
    body = body
    msg.attach(MIMEText(body, 'plain'))
    email_string = msg.as_string()

    return email_string


def send_email(smtp_server, email_string):
    smtp_server.sendmail(SETTINGS.get('SenderEmail', 'Email'), SETTINGS.get('DestinationEmail', 'Email'), email_string)


def main():
    server = create_server()
    email_string = create_email_string("Test", "Body test")
    send_email(server, email_string)
    print("test e-mail sent!")


if __name__ == "__main__":
    main()




