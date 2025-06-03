import pytest
from website.models import User
from website.models import Customer
from werkzeug.security import generate_password_hash
from website import db
from website import create_app


#Create the app so tests can take place
@pytest.fixture
def client():
    app = create_app()  
    with app.app_context():  
        yield app.test_client()  
        
@pytest.fixture
def login_as(client):
    def _login(user):
        with client.session_transaction() as sess:
            sess['_user_id'] = str(user.id)
    return _login

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

@pytest.fixture
def customer():
    customer = Customer(
        first_name="Tess",
        last_name="Tester",
        account_number="123456789",
        postcode="FY60BU"
    )
    db.session.add(customer)
    db.session.commit()
    yield customer
    db.session.delete(customer)
    db.session.commit()
