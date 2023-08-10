import json
import os
from abc import ABC, abstractmethod
import requests


class VacanciesAPI(ABC):
    @abstractmethod
    def get_vacancies(self, title: str):
        pass


class HeadHunterAPI(VacanciesAPI):
    """
    Класс, получающий данные по вакансиям HeadHunter по API.
    Дочерний класс VacanciesAPI.
    """

    def get_vacancies(self, title: str):
        """Возвращает список экземпляров класса Job"""
        params = {
            'text': title,
            'page': 7,
            'per_page': 100,
        }
        hh_response = requests.get('https://api.hh.ru/vacancies', params=params)  #.json()
        data = hh_response.json()
        job_list = []
        job_data = data['items']
        for job in job_data:
            title = job['name']

            if job['salary'] is None:
                salary = f'Зарплата не указана'
            elif job['salary']['from'] is None and job['salary']['to'] is not None:
                salary = f'Верхний порог зарплаты - {job["salary"]["to"]}'
            elif job['salary']['to'] is None and job['salary']['from'] is not None:
                salary = f'Нижний порог зарплаты - job["salary"]["from"]'
            else:
                salary = f'{job["salary"]["from"]} - {job["salary"]["to"]}'

            # salary = job['salary']['from'] if job['salary']['from'] is not None else 0
            description = job['snippet']['requirement']
            url = job['alternate_url']
            job_list.append({'title': title, 'salary': salary, 'description': description, 'url': url})

        with open('headhunter.json', 'a', encoding='utf-8') as f:
            json.dump(job_list, f, ensure_ascii=False, indent=2)


class SuperJobAPI(VacanciesAPI):
    """Класс, получающий данные по вакансиям SuperJob по API"""
    def get_vacancies(self, title: str):
        """Возвращает список экземпляров класса Job"""
        api_key = os.getenv('SUPERJOB_API_KEY')
        headers = {'Host': 'api.superjob.ru',
                   'X-Api-App-Id': api_key,
                   'Authorization': 'Bearer r.000000010000001.example.access_token',
                   'Content-Type': 'application/x-www-form-urlencoded'
                   }
        params = {
            'keyword': title,
            'page': 0,
            'count': 100
        }
        sj_response = requests.get('https://api.superjob.ru/2.0/vacancies/', params=params, headers=headers)
        data = sj_response.json()
        job_list = []
        job_data = data['objects']
        for job in job_data:
            title = job['profession']
            salary = job['payment_from'] if job['payment_from'] is not None else 0
            description = job['candidat']
            url = job['link']
            job_list.append({'title': title, 'salary': salary, 'description': description, 'url': url})

        with open('superjob.json', 'a', encoding='utf-8') as f:
            json.dump(job_list, f, ensure_ascii=False, indent=2)
