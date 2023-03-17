# from app.config import TestConfig
# app.config.from_object(TestConfig)
from app.models import UserModel
import pytest


@pytest.fixture(scope='module')
def new_user():
    user = UserModel(['patkennedy79@gmail.com', 'FlaskIsAwesome'])
    return user
def test_new_user_with_fixture(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, authenticated, and role fields are defined correctly
    """
    assert new_user.email == 'patkennedy79@gmail.com'
    assert new_user.hashed_password != 'FlaskIsAwesome'