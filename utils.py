from class_api import HeadHunterAPI, SuperJobAPI
from class_job import Job
from class_record import SaveToJSON


def interact_with_user():
    """Функция, которая выводит в консоль информацию о вакансиях пользователю"""

    user_name = input('Здравствуйте! Введите Ваше имя: ')
    while True:
        user_input = input(f'{user_name}, выберите платформу: 1 - HeadHunter, 2 - SuperJob, 3 - Выход. ')
        if user_input == '1':
            hh_query = input('Введите название интересующей вакансии:\n')
            hh_request = HeadHunterAPI()
            hh_data = hh_request.get_vacancies(hh_query)
            # print(hh_data)
            if not hh_data:
                print(f'{user_name}, по Вашему запросу ничего не найдено.')
            else:
                filtered_hh_data = [item for item in hh_data if item.get('salary') is not None]
                # sorted_data = sorted(filtered_hh_data, key=itemgetter('from'), reverse=True)
                sorted_data = sorted(filtered_hh_data, key=lambda x: x['salary']['from'] if x['salary']['from'] else 0, reverse=True)

                top_num_jobs = int(input('Введите число для вывода топ-N вакансий: '))
                show_top_jobs = sorted_data[:top_num_jobs]
                list_jobs = []
                for item in show_top_jobs:
                    job = Job(item['title'], item['salary'], item['description'], item['url'])
                    list_jobs.append(job)

                for job in list_jobs:
                    print(f'Название: {job.title}\n'
                          f'Зарплата: {job.salary}\n'
                          f'Описание: {job.description}\n'
                          f'Ссылка на вакансию: {job.url}\n')

                save_data = input(f'{user_name}, вы хотите сохранить данные?\n'
                                  f'Нажмите Y или N\n')
                if save_data.lower() == 'y':
                    save_to_json = SaveToJSON()
                    save_to_json.add_jobs_to_file(job.json_entry())
                else:
                    return None
        elif user_input == '2':
            superjob_query = input('Введите название интересующей вакансии:\n')
            sj_request = SuperJobAPI()
            sj_data = sj_request.get_vacancies(superjob_query)
            if not sj_data:
                print(f'{user_name}, по Вашему запросу ничего не найдено.')
            else:
                filtered_sj_data = [item for item in sj_data if item.get('salary') is not None]
                # sorted_data = sorted(filtered_sj_data, key=itemgetter('from'), reverse=True)
                sorted_data = sorted(filtered_sj_data, key=lambda x: x['salary'] if x['salary'] else 0, reverse=True)

                top_num_jobs = int(input('Введите число для вывода топ-N вакансий: '))
                show_top_jobs = sorted_data[:top_num_jobs]
                list_jobs = []
                for item in show_top_jobs:
                    job = Job(item['title'], item['salary'], item['description'], item['url'])
                    list_jobs.append(job)

                for job in list_jobs:
                    print(f'Название: {job.title}\n'
                          f'Зарплата: {job.salary}\n'
                          f'Описание: {job.description}\n'
                          f'Ссылка на вакансию: {job.url}\n')

                save_data = input(f'{user_name}, вы хотите сохранить данные?\n'
                                  f'Нажмите Y или N\n')
                if save_data.lower() == 'y':
                    save_to_json = SaveToJSON()
                    save_to_json.add_jobs_to_file(job.json_entry())
                else:
                    return None
        elif user_input == '3':
            print(f'Спасибо, {user_name}, хорошего дня!')
            break
        else:
            print(f'{user_name}, Вы ввели другое значение. Введите ещё раз. ')


print(interact_with_user())
