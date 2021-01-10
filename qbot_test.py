from Qbot import Qbot
from slack import WebClient
import os

slack_web_client = WebClient(token=os.environ.get("SLACK_TOKEN"))

Qbot = Qbot("bottesting")
slack_web_client.chat_postMessage(**Qbot.get_message_payload())
