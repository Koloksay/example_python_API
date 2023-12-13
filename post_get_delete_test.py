import sender_stand_request

# тестирование GET (в каждой позитивной проверке, нужно предварительно создавать запись в БД, чтобы тест
# был корректен, но так как нет возможности создавать новые записи, проверяем существующие

# Функция для позитивной проверки GET запроса по URL-параметру:
def positive_get_assert_code_200(parameter, value):
    # В переменную response сохраняется результат запроса на получение записи из таблицы:
    response = sender_stand_request.get_post_details(**{parameter: value})
    # Проверяется, что код ответа равен 200
    assert response.status_code == 200
    # Проверяем, что в теле ответа присутствует запись в формате "parameter": value
    assert any(post.get(parameter) == value for post in response.json())

# Функция для негативной проверки GET запроса на получение записи по URL-параметру:
def negative_get_assert_code_400(parameter, value):
    # Создаем словарь параметров и добавляем в него переданный параметр и значение
    params = {parameter: value}
    # Выполняем запрос с переданными параметрами
    response = sender_stand_request.get_post_details(**params)
    # Проверяем, что код ответа равен 400
    assert response.status_code == 400

# Функция для позитивной проверки POST запроса c определенным телом (без одного из параметров) :
def positive_no_parametr_post_assert_code_201(body):
    response = sender_stand_request.post_record_no_param(body)
    assert response.status_code == 201
    max_id = sender_stand_request.get_max_id()
    assert response.json()['id'] == max_id + 1

# Функция для позитивной проверки POST запроса:
def positive_post_assert_code_201(parameter, value):
    # В переменную response сохраняется результат запроса на получение записи из таблицы:
    response = sender_stand_request.post_record(parameter, value)
    # Проверяется, что код ответа равен 201
    assert response.status_code == 201
    # Проверяем, что в теле ответа присутствует запись в формате "parameter": "value"
    assert parameter in response.json() and response.json()[parameter] == value
    # Проверяем, что в теле ответа создана запись с номером id следующим за предыдущим
    max_id = sender_stand_request.get_max_id()
    assert response.json()['id'] == max_id + 1

# Функция для негативной проверки POST запроса на получение записи с определенным значением параметра:
def negative_post_assert_code_400(parameter, value):
    # В переменную response сохраняется результат запроса на получение записи из таблицы:
    response = sender_stand_request.post_record(parameter, value)
    # Проверяется, что код ответа равен 400
    assert response.status_code == 400

# Функция для негативной проверки POST запроса на получение записи с определенным телом (для отправки без параметра):
def negative_post_assert_no_param_400(body):
    # В переменную response сохраняется результат запроса на создание записи:
    response = sender_stand_request.post_record_no_param(body)
    # Проверяется, что код ответа равен 400
    assert response.status_code == 400

# Функция для позитивной проверки DELETE запроса на удаление записи:
def positive_delete_assert(id):
    response = sender_stand_request.delete_string_by_id(id)
    # Проверяем код ответа
    assert response.status_code == 200
    # Проверяем, что запись с заданным id отсутствует в базе
    get_response = sender_stand_request.get_post_details(id=id)
    assert get_response.status_code == 400

# Функция для негативной проверки DELETE запроса на удаление записи:
def negative_delete_assert_code_404(id):
    response = sender_stand_request.delete_string_by_id(id)
    # Проверяем, что в БД нет записи с таким ID
    get_response = sender_stand_request.get_post_details(id=id)
    assert get_response.status_code == 400
    # Проверяем код ответа
    assert response.status_code == 404

# Тест 1. Успешное создания записи
# параметр 'userId' корректный - число
def test_string_entry_when_the_userid_is_int_get_success_response():
    positive_post_assert_code_201('userId', 1)

# Тест 2. Успешное создания записи
# параметр 'body' корректный - строка
def test_string_entry_when_the_body_is_str_get_success_response():
    positive_post_assert_code_201('body', 'FfФф192381')

# Тест 3. Успешное создания записи
# параметр 'title' корректный - строка
def test_string_entry_when_the_title_is_str_get_success_response():
    positive_post_assert_code_201('title', 'FfФф192381')

# Тест 4. Успешное создания записи
# параметр 'id' корректный - число
def test_string_entry_when_the_id_is_int_get_success_response():
    positive_post_assert_code_201('id', 101)

# Тест 5. Успешное создания записи
# параметр 'id' не передан
def test_string_entry_when_the_is_no_param_id_get_error_response():
    body = {
        "userId": 12,
        "title": "Testing",
        "body": "123"
    }
    positive_no_parametr_post_assert_code_201(body)

# Тест 6. Ошибка "400" при создании
# параметр 'userId' неверный тип данных "строка"
def test_post_record_in_table_then_user_id_str_get_error_response():
    negative_post_assert_code_400('userId', 'один')

# Тест 7. Ошибка "400" при создании
# параметр 'userId' передано пустое значение
def test_string_entry_when_the_userid_is_none_get_error_response():
    negative_post_assert_code_400('userId', None)

# Тест 8. Ошибка "400" при создании
# параметр 'userId' не передан
def test_string_entry_when_the_userid_non_exist_get_error_response():
    body = {
        "title": "Testing",
        "body": "123"
    }
    negative_post_assert_no_param_400(body)

# Тест 9. Ошибка "400" при создании
# параметр 'userId' передано логически неверное значение (0)
def test_string_entry_when_the_userid_is_0_get_error_response():
    negative_post_assert_code_400('userId', 0)

# Тест 10. Ошибка "400" при создании записи
# параметр 'body' не передан
def test_string_entry_when_the_is_no_param_body_get_error_response():
    body = {
        "userId": 12,
        "title": "Testing"
    }
    negative_post_assert_no_param_400(body)

# Тест 11. Ошибка "400" при создании записи
# параметр 'title' не передан
def test_string_entry_when_the_is_no_param_title_get_error_response():
    body = {
        "userId": 12,
        "body": "123"
    }
    negative_post_assert_no_param_400(body)

# Тест 12. Ошибка "400" при создании записи
# параметр 'id' передано пустое значение
def test_string_entry_when_the_id_is_none_get_error_response():
    negative_post_assert_code_400('id', None)

# Тест 13. Ошибка "400" при создании записи
# параметр 'id' передан неверный тип данных - строка
def test_string_entry_when_the_id_is_str_get_error_response():
    negative_post_assert_code_400('id', 'сто')

# Тест 14. Ошибка "400" при создании записи
# передан уже существующий параметр 'id'
def test_string_entry_when_the_id_is_duplicate_get_error_response():
    negative_post_assert_code_400('id', 1)

# Тест 15. Ошибка "400" при создании записи
# передан логически неверный параметр 'id' (ноль)
def test_string_entry_when_the_id_is_0_get_error_response():
    negative_post_assert_code_400('id', 0)

# Тест 16. Ошибка "400" при создании записи
# передан логически неверный параметр 'id' (отрицательное число)
def test_string_entry_when_the_id_is_minus_get_error_response():
    negative_post_assert_code_400('id', -1)

# Тест 17. Ошибка "400" при создании записи
# параметр 'title' передано пустое значение
def test_string_entry_when_the_title_is_none_get_error_response():
    negative_post_assert_code_400('title', None)

# Тест 18. Ошибка "400" при создании записи
# параметр 'title' передан неверный тип данных (число)
def test_string_entry_when_the_title_is_int_get_error_response():
    negative_post_assert_code_400('title', 1)

# Тест 19. Ошибка "400" при создании записи
# параметр 'title' передан неверный тип данных (число - ноль)
def test_string_entry_when_the_title_is_0_get_error_response():
    negative_post_assert_code_400('title', 0)

# Тест 20. Ошибка "400" при создании записи
# параметр 'title' очень большое значение
def test_string_entry_when_the_title_is_too_much_get_error_response():
    negative_post_assert_code_400('title', 2**16*'a')

# Тест 21. Ошибка "400" при создании записи
# параметр 'body' передано пустое значение
def test_string_entry_when_the_body_is_none_get_error_response():
    negative_post_assert_code_400('body', None)

# Тест 22. Ошибка "400" при создании записи
# параметр 'body' передан неверный тип данных - число
def test_string_entry_when_the_body_is_int_get_error_response():
    negative_post_assert_code_400('body', 1)

# Тест 23. Ошибка "400" при создании записи
# параметр 'body' очень большое значение
def test_string_entry_when_the_body_is_too_much_get_error_response():
    negative_post_assert_code_400('body', 2**16*'a')

# Тест 24. Ошибка "400" при создании записи
# параметр 'body' передан неверный тип данных - число ('ноль')
def test_string_entry_when_the_body_is_0_get_error_response():
    negative_post_assert_code_400('body', 0)

# Тест 25. Успешное получение записи
# URL-параметр 'userId' существует
def test_string_entry_when_the_userid_is_exist_get_success_response():
    positive_get_assert_code_200('userId', 1)

# Тест 26. Успешное получение записи
# URL-параметр 'id' существует
def test_string_entry_when_the_id_is_exist_get_success_response():
    positive_get_assert_code_200('id', 1)

# Тест 27. Успешное получение записи
# URL-параметр 'title' существует
def test_string_entry_when_the_title_is_exist_get_success_response():
    positive_get_assert_code_200('title', 'qui est esse')

# Тест 28. Успешное получение записи
# URL-параметр 'body' существует
def test_string_entry_when_the_body_is_exist_get_success_response():
    value = 'et iusto sed quo iure\nvoluptatem occaecati omnis eligendi aut ad\nvoluptatem doloribus vel accusantium quis pariatur\nmolestiae porro eius odio et labore et velit aut'
    positive_get_assert_code_200('body', value)

# Тест 29. Ошибка 400 при запросе данных при несуществующем URL-параметре 'userId'
def test_string_entry_when_the_userid_is_no_exist_get_success_response():
    negative_get_assert_code_400('userId', 9999)

# Тест 30. Ошибка 400 при запросе данных при несуществующем URL-параметре 'id'
def test_string_entry_when_the_id_is_no_exist_get_success_response():
    negative_get_assert_code_400('id', 9999)

# Тест 31. Ошибка 400 при запросе данных при несуществующем URL-параметре 'title'
def test_string_entry_when_the_title_is_no_exist_get_error_response():
    negative_get_assert_code_400('title', 9999)

# Тест 32. Ошибка 400 при запросе данных при несуществующем URL-параметре 'body'
def test_string_entry_when_the_body_is_no_exist_get_error_response():
    negative_get_assert_code_400('body', 9999)

# Тестирование DELETE /post
# Тест 33. Успешное удаление записи. Передан корректный URL-параметр "id"
def test_string_delete_when_the_id_is_correct_get_success_response():
    positive_delete_assert(1)

# Тест 34. Передан несуществующий URL-параметр "id"
def test_string_delete_when_the_id_is_incorrect_get_error_response():
    negative_delete_assert_code_404(999)