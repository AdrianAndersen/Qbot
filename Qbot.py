

class Qbot():
    MESSAGE_BLOCK = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": (
                "Fakk deg....\n\n"
            ),
        },
    }

    def __init__(self, channel):
        self.channel = channel

    def get_message_payload(self):
        return {
            "channel": self.channel,
            "blocks": [
                self.MESSAGE_BLOCK
            ],
        }
