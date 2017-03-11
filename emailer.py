import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import configparser

SETTINGS = configparser.ConfigParser()
SETTINGS.read('email.ini')


def createServer():
    user = SETTINGS.get('SenderEmail', 'Email')
    password = SETTINGS.get('SenderEmail', 'Password')
    smtpServer = smtplib.SMTP_SSL(SETTINGS.get('SenderEmail', 'Server'))
    smtpServer.login(user, password)
    return smtpServer


def createEmailString(subject, body):
    msg = MIMEMultipart()
    msg['From'] = SETTINGS.get('SenderEmail', 'Name') + " <" + SETTINGS.get('SenderEmail', 'Email') + ">"
    msg['To'] = SETTINGS.get('DestinationEmail', 'Email')
    msg['Subject'] = subject
    body = body
    msg.attach(MIMEText(body, 'plain'))
    emailString = msg.as_string()

    return emailString


def sendEmail(smtpServer, emailString):
    smtpServer.sendmail(SETTINGS.get('SenderEmail', 'Email'), SETTINGS.get('DestinationEmail', 'Email'), emailString)


def main():
    server = createServer()
    emailString = createEmailString("Test", "Body test")
    sendEmail(server, emailString)
    print("test e-mail sent!")


if __name__ == "__main__":
    main()




