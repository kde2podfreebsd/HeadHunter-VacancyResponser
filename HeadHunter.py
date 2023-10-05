import os
import json

import requests
from dotenv import load_dotenv
from TokenManager import TokenManager
from datetime import datetime, timedelta


class HeadHunterAdapter:

    @staticmethod
    def refreshAccessToken():

        if os.path.isfile('tokens.json'):
            with open(file="tokens.json", mode="r") as tokens:
                tok = json.load(tokens)

        load_dotenv()

        data = {
            'grant_type': 'refresh_token',
            'client_id': os.getenv("client_id"),
            'client_secret': os.getenv("client_secret"),
            'refresh_token': tok['refresh_token'],
        }

        response = requests.post('https://hh.ru/oauth/token', data=data)

        if response.status_code == 400:
            pass

        else:

            response_data = response.json()
            new_access_token = response_data['access_token']
            new_refresh_token = response_data['refresh_token']
            expires_in = response_data['expires_in']
            new_date = datetime.now() + timedelta(seconds=expires_in)

            TokenManager.uploadTokens(
                access_token=new_access_token,
                refresh_token=new_refresh_token,
                expires_in=str(new_date)
            )

    @staticmethod
    def getActiveVacanciesIds(employer_id: int, access_token: str):

        headers = {'Authorization': f'Bearer {access_token}'}
        url = f'https://api.hh.ru/employers/{employer_id}/vacancies/active'

        response = requests.get(url, headers=headers)

        vacancies_ids = list()

        data = response.json()

        for x in data['items']:
            vacancies_ids.append(x['id'])

        return vacancies_ids

    @staticmethod
    def getNegotiationsByVacanciesId(vacancy_id: int, access_token: str):

        headers = {'Authorization': f'Bearer {access_token}'}
        url = f'https://api.hh.ru/negotiations/response?vacancy_id={vacancy_id}'

        response = requests.get(url, headers=headers)

        output = list()

        if response.status_code == 200:
            data = response.json()

            for x in data['items']:
                output.append({"id": x["id"], "name": x['resume']['first_name']})
            return output
        else:
            pass

    @staticmethod
    def sendMessageToNegotiation(negotiation_id: int, message: str, access_token: str):

        headers = {'Authorization': f'Bearer {access_token}'}
        data = {"message": message}
        url = f"https://api.hh.ru/negotiations/{negotiation_id}/messages"

        response = requests.post(url, headers=headers, data=data)

        if response.status_code == 201:
            return True