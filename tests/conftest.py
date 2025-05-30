import pytest
from website.models import User
from werkzeug.security import generate_password_hash
from website import db
from website import create_app

#Create the app so tests can take place
@pytest.fixture
def client():
    app = create_app()  
    with app.app_context():  
        yield app.test_client()  

#Create fake test user to use in other tests
@pytest.fixture
def test_user():
    user = User(
        email='testuser@example.com',
        password=generate_password_hash('CorrectPassword123'),
        first_name='Test',
        last_name='User'
    )
    db.session.add(user)
    db.session.commit()
    yield user
    db.session.delete(user)
    db.session.commit()
