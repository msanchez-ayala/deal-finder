import os
import smtplib
import ssl
from email import message
from datetime import date


EMAIL_SENDER_ADDRESS = os.environ.get('EMAIL_SENDER_ADDRESS')
EMAIL_SENDER_PASSWORD = os.environ.get('EMAIL_SENDER_PASSWORD')
EMAIL_RECEIVER_ADDRESS = os.environ.get('EMAIL_RECEIVER_ADDRESS')
SUBJECT = 'Lululemon search results'


def validate_env_vars() -> None:
    if any(env_var is None for env_var in
           (EMAIL_SENDER_ADDRESS,
            EMAIL_RECEIVER_ADDRESS,
            EMAIL_SENDER_PASSWORD)):
        raise OSError('ERROR: Expected environment variables to exist for the '
                      f'following: {EMAIL_SENDER_ADDRESS=}, '
                      f'{EMAIL_RECEIVER_ADDRESS=}, and '
                      f'{EMAIL_SENDER_PASSWORD=}.')


def make_message(body: str) -> message.EmailMessage:
    validate_env_vars()
    msg = message.EmailMessage()
    msg['From'] = EMAIL_SENDER_ADDRESS
    msg['To'] = EMAIL_RECEIVER_ADDRESS
    msg['Subject'] = SUBJECT
    msg.set_content(body)
    return msg


def send_message(msg: message.EmailMessage) -> None:
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(host='smtp.gmail.com', context=context) as server:
        server.login(user=EMAIL_SENDER_ADDRESS, password=EMAIL_SENDER_PASSWORD)
        server.send_message(msg)


if __name__ == '__main__':
    msg = make_message('test email')
    send_message(msg)


