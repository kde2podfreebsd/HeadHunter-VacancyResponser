import time
import schedule

from HeadHunter import HeadHunterAdapter
from TokenManager import TokenManager
from MessagesJournal import MessageJournalAdapter


def job(employer_id: int):
    tokens = TokenManager.downloadTokens()

    active_vacancies = HeadHunterAdapter.getActiveVacanciesIds(
        employer_id=employer_id,
        access_token=tokens['access_token']
    )

    for vacancy_id in active_vacancies:
        negotiations = HeadHunterAdapter.getNegotiationsByVacanciesId(
            vacancy_id=vacancy_id,
            access_token=tokens['access_token']
        )

        messages = MessageJournalAdapter.load_sent_messages()

        sent_ids = set(item['id'] for item in messages['message_journal'])

        new_data = [{'name': x['name'], 'id': x['id'], "vacancy_id": vacancy_id, "is_sent": True}
                    for x in negotiations if x['id'] not in sent_ids]

        for x in new_data:
            print(f"send msg to {x['id']} {x['name']}")
            # HeadHunterAdapter.sendMessageToNegotiation(
            #     negotiation_id=x['id'],
            #     message="test",
            #     access_token=tokens['access_token']
            # )

        messages['message_journal'].extend(new_data)

        MessageJournalAdapter.save_sent_messages(messages)



if __name__ == "__main__":
    job(employer_id=9845326)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)