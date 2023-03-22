import pytest
from flask import url_for
from flask_login import current_user,login_user

from app import create_app, login_manager
from app.config import TestConfig, DevelopmentConfig
from app.models import db, UserModel, get_current_timestamp
from unittest.mock import MagicMock


def setup_module(module):
    # Создание тестовой базы данных и добавление тестового пользователя
    app = create_app()
    app.config.from_object(DevelopmentConfig)

    #создание пользователя
    # with app.app_context():
    #     user = UserModel(username="admin2",email="asd@qwer.net", password="admin",date_create=get_current_timestamp().replace(microsecond=0).isoformat(' '))
    #     db.session.add(user)
    #     db.session.commit()

def teardown_module(module):
    # Очистка тестовой базы данных
    app = create_app()
    app.config.from_object(DevelopmentConfig)
    #удаление базы
    # with app.app_context():
    #     db.drop_all()

@pytest.fixture
def app():
    # Создание приложения Flask с настройками для тестирования
    app = create_app()
    app.config.from_object(DevelopmentConfig)
    return app

@pytest.fixture
def client(app):
    # Создание тестового клиента Flask для приложения
    client = app.test_client()
    return client


def test_signin(client,app, mocker):
    # Создание тестового пользователя
    test_user = {"username": "admin", "password": "admin"}
    print(test_user['username'])

    # Создание мок объекта для модели пользователя
    # user_mock = MagicMock(spec=UserModel)
    #
    # # Настройка мок объекта для метода проверки пароля
    # user_mock.check_password.return_value = True
    #
    # # Настройка мок объекта для метода поиска пользователя в БД
    # mocker.patch("app.models.UserModel.query", return_value=user_mock)

    user = (UserModel.query.filter_by(username=test_user['username']).first())
    # Отправка POST запроса с данными тестового пользователя
    #response = client.post('/signin/', data=test_user, follow_redirects=True)
    login_user(user, remember=True, force=True)

    response = client.get('/signin/')
    # Проверка, что запрос был успешным (код 200)
    assert response.status_code == 200
    # print(current_user)
    assert current_user.username == 'admin'

    # Проверка, что пользователь успешно авторизован
    assert b"Welcome to your twis" in response.data

    # # Проверка вызова метода поиска пользователя в БД с указанным именем пользователя
    # UserModel.query.filter_by.assert_called_once_with(username=test_user["username"])
    #
    # # Проверка вызова метода проверки пароля у найденного пользователя
    # user_mock.check_password.assert_called_once_with(test_user["password"])

def test_logout(client):
    # Пользователь должен быть выведен из системы при выходе
    response = client.get('/logout', follow_redirects=True)
    assert current_user.is_anonymous