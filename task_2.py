''' В нашей школе мы не можем разглашать персональные данные пользователей, но чтобы преподаватель и ученик
смогли объяснить нашей поддержке, кого они имеют в виду  (у преподавателей, например, часто учится несколько Саш),
мы генерируем пользователям уникальные и легко произносимые имена. Имя у нас состоит из прилагательного, имени животного
и двузначной цифры. В итоге получается, например, "Перламутровый лосось 77".
Для генерации таких имен мы и решали следующую задачу:
Получить с русской википедии список всех животных (https://inlnk.ru/jElywR) и
вывести количество животных на каждую букву алфавита. Результат должен получиться в следующем виде:

А: 642
Б: 412
В:....
'''

import json
from collections import defaultdict
import requests


def task():
    session = requests.Session()
    url = 'https://ru.wikipedia.org/w/api.php'
    params = {
        'action': 'query',
        'format': 'json',
        'list': 'categorymembers',
        'cmtitle': 'Категория:Животные по алфавиту',
        'cmlimit': 500
    }
    ru_upper = set('АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ')
    result = defaultdict(list)

    flag = True

    while flag:
        try:
            res = session.get(url, params=params)
            data = res.json()

            for animal in data['query']['categorymembers']:
                if animal['title'][0] in ru_upper:
                    result[animal['title'][0]].append(animal['title'])

            if 'continue' in data:
                params['cmcontinue'] = data.get('continue').get('cmcontinue')
            else:
                flag = False
        except requests.exceptions.RequestException as e:
            print(e)
            flag = False

    result = dict(sorted(result.items(), key=lambda x: x[0]))

    write_to_file(result)
    print_result(result)


def write_to_file(data):
    with open('animals.json', 'w', encoding="utf-8") as file:
        json.dump(data, file)


def print_result(data):
    for _, key in enumerate(data):
        print(f'{key}: {len(data[key])}')


task()
