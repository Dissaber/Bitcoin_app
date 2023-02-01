# -- coding: utf-8 --
import copy

import database
import pydantic_models
import config
import fastapi
from fastapi import Request

api = fastapi.FastAPI()

fake_database = {'users':[
    {
        "id":1,
        "name":"Anna",
        "nick":"Anny42",
        "balance": 15300
     },

    {
        "id":2,
        "name":"Dima",
        "nick":"dimon2319",
        "balance": 160.23
     }
    ,{
        "id":3,
        "name":"Vladimir",
        "nick":"Vova777",
        "balance": 200.1
     }
],}


@api.put('/user/{user_id}')
def update_user(user_id: int, user: pydantic_models.User = fastapi.Body()):
    for index, user_upd in enumerate(fake_database['users']):
        if user_upd['id'] == user_id:
            fake_database['users'][index] = user  # обновляем юзера в бд по соответствующему ему индексу из списка users
            return user


@api.delete('/user/{user_id}')
def delete_user(user_id: int = fastapi.Path()):
    for index, user_del in enumerate(fake_database['users']):
        if user_del['id'] == user_id:
            old_db = copy.deepcopy(fake_database)
            del  fake_database['users'][index]
            return {'old_db': old_db,
                    'new_db': fake_database}

@api.post('/user/create')
def index(user: pydantic_models.User):
    """
        Когда в пути нет никаких параметров
        и не используются никакие переменные,
        то fastapi, понимая, что у нас есть аргумент, который
        надо заполнить, начинает искать его в теле запроса,
        в данном случае он берет информацию, которую мы ему отправляем
        в теле запроса и сверяет её с моделью pydantic, если всё хорошо,
        то в аргумент user будет загружен наш объект, который мы отправим
        на сервер.
        """
    fake_database['users'].append(dict(user))
    return {'User Created': user}

@api.get('/get_info_by_user_id/{id:int}')
def get_info_about_user(id):
    return fake_database['users'][id - 1]


@api.get('/get_user_balance_by_id/{id:int}')
def get_user_balance(id):
    return fake_database['users'][id - 1]['balance']


@api.get('/get_total_balance')
def get_total_balance():
    total_balance: float = 0.0
    for user in fake_database['users']:
        total_balance += pydantic_models.User(**user).balance
    return total_balance


@api.get("/users/")
def get_users(skip: int = 0, limit: int = 10):
    """
    аргументы skip(пропуск) и limit(ограничение) будут браться из пути,
    который запрашивает пользователь, добавляются они после знака вопроса "?"
    и перечисляются через амперсанд "&", а их значения задаются через знак равно "=",
    то есть, чтобы задать значения аргументам skip=1 и limit=10 нам нужно выполнить GET-запрос,
    который будет иметь путь "/users?skip=1&limit=10"
    """
    return fake_database['users'][skip: skip + limit]


@api.get("/user/{user_id}")
def read_user(user_id: str, query: str | None = None):
    """

    :param user_id: Строка
    :param query: по умолчанию None
    :return: json
    """
    if query:
        return {"user_id": user_id, "query": query}
    return {"user_id": user_id}


