import typing

from airq import config
from airq.commands.base import ApiCommandHandler
from airq.lib.ses import send_email
from airq.models.events import EventType
from airq.models.clients import Client

class ShowFeedbackHandler(ApiCommandHandler):
    def handle(self) -> typing.List[str]:
        message = [
            "Please enter your feedback below:"  # consider adding cancel option
        ]
        self.client.log_event(EventType.FEEDBACK_BEGIN)
        return message



class RecieveFeedbackHandler(ApiCommandHandler):
    @classmethod
    def should_handle(cls, pattern: str, client: Client, user_input: str) -> bool:
        return client.should_accept_feedback()

    def handle(self) -> typing.List[str]:
        print(self.user_input)
        send_email(
            config.ADMIN_EMAILS,
            'Client gave feedback',
            self.user_input
        )
        message = [
            "Thank you for your feedback!"
        ]
        self.client.log_event(EventType.FEEDBACK_RECIEVED)
        return message