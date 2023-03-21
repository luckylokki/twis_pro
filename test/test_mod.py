# Импортируем необходимые библиотеки
from flask_login import login_user
from flask_sqlalchemy.session import Session

from app import create_app
from app.models import UserModel


# Создаем фикстуру create_app
def test_client():
    app = create_app()
    with app.test_client() as client:
        with app.app_context():
            yield client


# Создаем тестовый класс TestSignIn
class TestSignIn:
    # Тест для успешной аутентификации пользователя
    def test_successful_signin(self, test_client):
        # Создаем сессию и добавляем пользователя в базу данных
        session = Session()
        user = UserModel(username='admin', password='admin')
        # session.add(user)
        session.commit()

        # Отправляем POST-запрос для входа пользователя
        response = test_client.post('/login', data=dict(
            username='admin',
            password='admin'
        ), follow_redirects=True)

        # Проверяем, что пользователь успешно вошел
        assert response.status_code == 200
        assert b'Logged in successfully!' in response.data

    # Тест для неуспешной аутентификации пользователя
    def test_unsuccessful_signin(self, test_client):
        # Создаем сессию и добавляем пользователя в базу данных
        session = Session()
        user = UserModel(username='testuser', password='testpassword')
        session.add(user)
        session.commit()

        # Отправляем POST-запрос с неправильным паролем
        response = test_client.post('/login', data=dict(
            username='testuser',
            password='wrongpassword'
        ), follow_redirects=True)

        # Проверяем, что пользователь не может войти
        assert response.status_code == 200
        assert b'Invalid username or password' in response.data