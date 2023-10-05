import time
from datetime import datetime
import schedule
import os
import json
import logging

from HeadHunter import HeadHunterAdapter
from TokenManager import TokenManager
from MessagesJournal import MessageJournalAdapter

logging.basicConfig(filename='TokenManager.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def job(vacancy_id: int, message: str):
    try:
        tokens = TokenManager.downloadTokens()

        logging.info("Get tokens pair")

        ### For all active vacancies

        # active_vacancies = HeadHunterAdapter.getActiveVacanciesIds(
        #     employer_id=employer_id,
        #     access_token=tokens['access_token']
        # )
        #
        # for vacancy_id in active_vacancies:

        negotiations = HeadHunterAdapter.getNegotiationsByVacanciesId(
            vacancy_id=vacancy_id,
            access_token=tokens['access_token']
        )

        logging.info(f"get negotiations for vacancy: {vacancy_id}")

        messages = MessageJournalAdapter.load_sent_messages()

        sent_ids = set(item['id'] for item in messages['message_journal'])

        new_data = [
            {
                'name': x['name'],
                'id': x['id'],
                "vacancy_id": vacancy_id,
                "is_sent": True
            } for x in negotiations if x['id'] not in sent_ids
        ]

        logging.info(f"New negotiation for mailing {new_data}")

        for x in new_data:
            msg = message.replace("{name}", x['name'] if x['name'] is not None else "")
            HeadHunterAdapter.sendMessageToNegotiation(
                negotiation_id=x['id'],
                message=msg,
                access_token=tokens['access_token']
            )
            logging.info(f"Sent message for - id: {x['id']}, name: {x['name']}, message: {msg}")

        messages['message_journal'].extend(new_data)

        MessageJournalAdapter.save_sent_messages(messages)

        logging.info("extend sent messages to messages Journal")

    except Exception as e:
        logging.error(e)


def refresh_token():
    if os.path.isfile('tokens.json'):
        with open(file="tokens.json", mode="r") as tokens:
            tok = json.load(tokens)

        date_format = "%Y-%m-%d %H:%M:%S.%f"
        date_object = datetime.strptime(tok['expires_in'], date_format)

        if datetime.now() >= date_object:
            HeadHunterAdapter.refreshAccessToken()
            logging.info("refresh tokens pair")
        else:
            logging.info("not time yet for update tokens pair")


def main():
    if os.path.isfile('config.json'):
        with open(file="config.json", mode="r") as config_file:
            config = json.load(config_file)

    schedule.every(10).seconds.do(refresh_token)

    for x in config['items']:
        schedule.every(10).seconds.do(job, vacancy_id=x['vacancy_id'], message=x['message'])


if __name__ == "__main__":
    main()

    while True:
        schedule.run_pending()
        time.sleep(1)
