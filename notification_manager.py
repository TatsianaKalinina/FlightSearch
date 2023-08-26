import os
from twilio.rest import Client

TO = os.environ['TO']
TWILIO_VIRTUAL_NUMBER = os.environ['TWILIO_VIRTUAL_NUMBER']


class NotificationManager:

    def __init__(self):
        account_sid = os.environ['TWILIO_ACC_SID']
        auth_token = os.environ['TWILIO_AUTH_TOKEN']
        self.client = Client(account_sid, auth_token)

    def send_notifications(self, sms):
        message = self.client.messages.create(
            body=sms,
            from_=TWILIO_VIRTUAL_NUMBER,
            to=TO,
        )
        # Prints if successfully sent.
        print(message.sid)

