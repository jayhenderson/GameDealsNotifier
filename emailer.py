import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os import environ

def create_server():
    user = environ.get('SENDEREMAIL')
    password = environ.get('SENDERPASSWORD')
    smtp_server = smtplib.SMTP_SSL(environ.get('SENDEREMAIL'))
    smtp_server.login(user, password)
    return smtp_server


def create_email_string(subject, body):
    msg = MIMEMultipart()
    msg['From'] = "{} <{}>".format(environ.get('SENDERNAME'), environ.get('SENDEREMAIL'))
    msg['To'] = environ.get('DESTINATIONEMAIL')
    msg['Subject'] = subject
    body = body
    msg.attach(MIMEText(body, 'plain'))
    email_string = msg.as_string()

    return email_string


def send_email(smtp_server, email_string):
    smtp_server.sendmail(environ.get('SENDEREMAIL'),
                         environ.get('DESTINATIONEMAIL'),
                         email_string)


def main():
    server = create_server()
    email_string = create_email_string("Test", "Body test")
    send_email(server, email_string)
    print("test e-mail sent!")


if __name__ == "__main__":
    main()




