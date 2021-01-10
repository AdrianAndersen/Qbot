import os
import logging
from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from Qbot import Qbot


# Initialize a Flask app to host the events adapter
app = Flask(__name__)

# Create an events adapter and register it to an endpoint in the slack app for event ingestion.
slack_events_adapter = SlackEventAdapter(
    os.environ.get("SLACK_EVENTS_TOKEN"), "/slack/events", app)
slack_web_client = WebClient(token=os.environ.get("SLACK_TOKEN"))

if __name__ == "__main__":
    # Create the logging object
    logger = logging.getLogger()

    # Set the log level to DEBUG. This will increase verbosity of logging messages
    logger.setLevel(logging.DEBUG)

    # Add the StreamHandler as a logging handler
    logger.addHandler(logging.StreamHandler())

    # Run your app on your externally facing IP address on port 3000 instead of
    # running it on localhost, which is traditional for development.
    app.run(host='0.0.0.0', debug=True, port=3000)


def post_test_message(channel):
    """Craft the qbot and send the message to the channel
    """
    # Create a new qbot
    qbot = Qbot(channel)

    # Get the onboarding message payload
    message = qbot.get_message_payload()

    # Post the onboarding message in Slack
    slack_web_client.chat_postMessage(**message)

# When a 'message' event is detected by the events adapter, forward that payload
# to this function.


@slack_events_adapter.on("message")
def message(payload):
    """Parse the message event, and if the activation string is in the text,
    send the result.
    """

    # Get the event data from the payload
    event = payload.get("event", {})

    # Get the text from the event that came through
    text = event.get("text")

    # Check and see if the activation phrase was in the text of the message.
    # If so, execute the code to flip a coin.
    if "qbot er teit" in text.lower():
        # Since the activation phrase was met, get the channel ID that the event
        # was executed on
        channel_id = event.get("bottesting")

        # Execute the flip_coin function and send the results of
        # flipping a coin to the channel
        return post_test_message(channel_id)
