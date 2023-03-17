from app import app
from app.models import UserModel
import pytest


@pytest.fixture(scope='module')
def new_user():
    user = UserModel('patkennedy79@gmail.com', 'FlaskIsAwesome')
    return user

class TestViews:

    # Каждый тест изолирован - не зависит от другого
    def setup_method(self):
        #print('Я выполняюсь перед каждый тестом')
        # app.testing = True
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get('/')
        # 1. Код ответа
        # 2. Права пользователя
        # 3. На странице есть данные
        # 4. Проверка как работают формы
        assert response.status_code == 302

    def test_home_page_post_with_fixture(new_user):
        """
        GIVEN a Flask application
        WHEN the '/' page is is posted to (POST)
        THEN check that a '405' status code is returned
        """
        response = new_user.post('/')
        assert response.status_code == 405
    def test_signin(self):
        response = self.client.get('/signin/')
        assert response.status_code == 200
    def test_signup(self):
        response = self.client.get('/signup/')
        assert response.status_code == 200

    def teardown_method(self):
        #print('А я после каждого теста')
        pass

