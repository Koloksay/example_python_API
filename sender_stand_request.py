import configuration
import requests
import data

# удаление записи по id
def delete_string_by_id(id):
    delete_url = f'{configuration.URL_SERVICE + configuration.TABLE_PATH}/{id}'
    response = requests.delete(delete_url)
    return response

# получение информации о записи по параметрам id, userId, title, body
def get_post_details(id=None, userId=None, title=None, body=None):
    params = {}
    if id is not None:
        params['id'] = id
    if userId is not None:
        params['userId'] = userId
    if title is not None:
        params['title'] = title
    if body is not None:
        params['body'] = body

    response = requests.get(configuration.URL_SERVICE + configuration.TABLE_PATH, params=params)
    return response

# создание новой записи с телом с одним измененным параметром
def post_record(parameter, value):
    current_body = data.body.copy()
    current_body[parameter] = value
    # Отправляем POST запрос на создание записи с телом из файла data.py
    response = requests.post(configuration.URL_SERVICE + configuration.TABLE_PATH,
                             json=current_body)
    # Возвращаем ответ
    return response

# получение максимального значения id
def get_max_id():
    response = requests.get(configuration.URL_SERVICE + configuration.TABLE_PATH)
    if response.status_code == 200:
        data = response.json()
        max_id = max(record['id'] for record in data)
        return max_id
    else:
        # Обработка случая, когда запрос не удался
        print('Ошибка при получении данных')
        return None

# создание новой записи с определенным телом
def post_record_no_param(body):
    # Отправляем POST запрос на создание записи с телом из файла data.py
    response = requests.post(configuration.URL_SERVICE + configuration.TABLE_PATH,
                             json=body)
    # Возвращаем ответ
    return response