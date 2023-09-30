import os
import json
from HeadHunter import HeadHunterAdapter

basedir = os.path.abspath(os.path.dirname(__file__))


class TokenManager:

    @staticmethod
    def upload_tokens():
        session_file_path = os.path.join(basedir, "tokens.json")

        if os.path.isfile(session_file_path):
            with open(file="tokens.json", mode="r") as tokens:
                return json.load(tokens)

    @staticmethod
    def createJsonTokenStruct():

        data = {
            "access_token": "",
            "refresh_token": "",
            "expired_at": ""
        }

        session_file_path = os.path.join(basedir, "tokens.json")

        if not os.path.isfile(session_file_path):
            with open('tokens.json', 'w') as outfile:
                json.dump(data, outfile)



    # @staticmethod
    # def refreshTokens():
