import typing

from airq.commands.base import RegexCommand
from airq.models.zipcodes import Zipcode


class Resubscribe(RegexCommand):
    pattern = r"^(y|yes)$"

    def handle(self) -> typing.List[str]:
        if self.client.zipcode is None:
            return self._get_missing_zipcode_message()

        if self.client.is_enabled_for_alerts:
            return [
                f"Looks like you're already watching {self.client.zipcode.zipcode}."
            ]

        self.client.enable_alerts()

        return [
            f"Got it! We'll send you timely alerts when air quality in {self.client.zipcode.zipcode} changes category."
        ]
