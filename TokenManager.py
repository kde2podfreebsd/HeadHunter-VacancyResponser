import datetime
import os
import json

basedir = os.path.abspath(os.path.dirname(__file__))


class TokenManager:

    @staticmethod
    def downloadTokens():
        session_file_path = os.path.join(basedir, "tokens.json")

        if os.path.isfile(session_file_path):
            with open(file="tokens.json", mode="r") as tokens:
                return json.load(tokens)

    @staticmethod
    def uploadTokens(access_token: str, refresh_token: str, expires_in: str):

        token_data = TokenManager.downloadTokens()
        token_data['access_token'] = access_token
        token_data['refresh_token'] = refresh_token
        token_data['expires_in'] = expires_in

        session_file_path = os.path.join(basedir, "tokens.json")

        if os.path.isfile(session_file_path):
            with open('tokens.json', 'w') as outfile:
                json.dump(token_data, outfile, indent=4)

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