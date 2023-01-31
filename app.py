# -- coding: utf-8 --

response = {'Ответ': 'Который возвращает сервер'}

import fastapi
import database
import pydantic_models
import config

api = fastapi.FastAPI()

fake_database = {'users': [

    {
        "id": 1,  # число
        "name": "Anna",  # строка
        "nick": "Anny42",  # строка
        "balance": 15300  # int
    },

    {
        "id": 2,
        "name": "Dima",
        "nick": "dimon2319",
        "balance": 160.23  # float
    }
    , {
        "id": 3,
        "name": "Vladimir",
        "nick": "Vova777",
        "balance": "25000"  # нестандартный тип данных в его балансе
    }
], }


@api.get('/get_info_by_user_id/{id:int}')
def get_info_about_user(id):
    return fake_database['users'][id - 1]


@api.get('/get_user_balance_by_id/{id:int}')
def get_user_balance(id):
    return fake_database['users'][id - 1]['balance']


@api.get('/get_user_name_by_id/{id:int}')
def get_user_name_by_id(id):
    return fake_database['users'][id - 1]['name']


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