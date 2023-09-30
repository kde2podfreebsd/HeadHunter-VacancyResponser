import os

import requests
from dotenv import load_dotenv


class HeadHunterAdapter:

    @staticmethod
    def refreshAccessToken():

        load_dotenv()

        data = {
            'grant_type': 'refresh_token',
            'client_id': os.getenv("client_id"),
            'client_secret': os.getenv("client_secret"),
            'refresh_token': 'Ваш_refresh_токен',
        }

        response = requests.post('https://hh.ru/oauth/token', data=data)

        if response.status_code == 400:
            # обработать {"error": "invalid_grant", "error_description": "token not expired"}
            return

        response_data = response.json()
        new_access_token = response_data['access_token']
        new_refresh_token = response_data['refresh_token']
        print("Новый access token:", new_access_token)
        print("Новый refresh token:", new_refresh_token)

    @staticmethod
    def getActiveVacanciesIds(employer_id: int, access_token: str):

        headers = {'Authorization': f'Bearer {access_token}'}
        url = f'https://api.hh.ru/employers/{employer_id}/vacancies/active'

        response = requests.get(url, headers=headers)

        data = response.json()
        print(data)

    @staticmethod
    def getNegotiationsByVacanciesId(vacancy_id: int, access_token: str):

        headers = {'Authorization': f'Bearer {access_token}'}
        url = f'https://api.hh.ru/negotiations/response?vacancy_id={vacancy_id}'

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            print(data)

        else:
            pass

    @staticmethod
    def sendMessageToNegotiation(negotiation_id: int, message: str, access_token: str):

        headers = {'Authorization': f'Bearer {access_token}'}
        data = {"message": message}
        url = f"https://api.hh.ru/negotiations/{negotiation_id}/messages"

        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 201:
            print("sended")