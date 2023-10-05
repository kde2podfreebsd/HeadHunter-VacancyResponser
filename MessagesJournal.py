import os
import json

basedir = os.path.abspath(os.path.dirname(__file__))


class MessageJournalAdapter:

    @staticmethod
    def load_sent_messages():
        SENT_MESSAGES_FILE = "sent_messages.json"

        try:
            with open(SENT_MESSAGES_FILE, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            with open(SENT_MESSAGES_FILE, 'w') as outfile:
                json.dump({}, outfile)

            return {}

    @staticmethod
    def save_sent_messages(sent_messages):
        SENT_MESSAGES_FILE = "sent_messages.json"

        with open(SENT_MESSAGES_FILE, "w") as file:
            json.dump(sent_messages, file, indent=4)
