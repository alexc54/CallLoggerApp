from website.views.calls.validation import validate_call_data
from website.views.calls.validation import validate_postcode
from website.views.auth.user_validation import validate_user_details

#Test to see if the login page loads when application is opened
def test_login_page_loads(client):
    response = client.get('/login')  
    assert response.status_code == 200  #Checks the page has loaded correctly
    #Below checks to make sure email,password,login fields are loaded on the page.
    assert b'Email' in response.data   
    assert b'Password' in response.data  
    assert b'Login' in response.data    
    #Below checks form element is on the page 
    assert b'<form' in response.data   
    
#Register Page loads
def test_register_page_loads(client):
    response = client.get('/register')  
    assert response.status_code == 200  #Check that the page loads correctly
    #Below checks, firstname,surname,email,password and register is displayed on the page
    assert b'First Name' in response.data
    assert b'Surname' in response.data
    assert b'Email' in response.data
    assert b'Enter your password' in response.data 
    assert b'Register' in response.data     
    #Below checks if a form displays 
    assert b'<form' in response.data 
    
    
#Input Call Validation
def test_validate_call_data_valid():
    errors = validate_call_data(
        customer_first_name="John",
        customer_last_name="Smith",
        account_number="123456789",
        postcode="FY6 0NN",
        reason_called="Sale"
    )
    assert errors == []

def test_validate_call_data_with_short_first_name():
    errors = validate_call_data(
        customer_first_name="J",
        customer_last_name="Smith",
        account_number="123456789",
        postcode="FY6 0NN"
    )
    assert "Customer First Name must be at least 3 characters long!" in errors

def test_validate_call_data_with_short_account_number():
    errors = validate_call_data(
        customer_first_name="John",
        customer_last_name="Smith",
        account_number="12356A",
        postcode="FY6 0NN"
    )
    assert any("Invalid Account Number" in e for e in errors)

def test_validate_postcode_invalid():
    assert validate_postcode("9876") == "Invalid Postcode!"


    
#User Validation

def test_valid_data(client):
    errors = validate_user_details("John", "Smith", "jsmith@testing.com", user_id=None)
    assert errors == []

def test_invalid_first_name(client):
    errors = validate_user_details("123", "Smith", "jsmith@testing.com", user_id=None)
    assert "First name must contain only letters!" in errors

def test_invalid_last_name(client):
    errors = validate_user_details("John", "123", "jsmith@testing.com", user_id=None)
    assert "Surname must contain only letters!" in errors

def test_short_email(client):
    errors = validate_user_details("John", "Smith", "j@t", user_id=None)
    assert "Email must be greater than 3 characters." in errors

def test_short_first_name(client):
    errors = validate_user_details("j", "Smith", "jsmith@testing.com", user_id=None)
    assert "First name must be greater than 1 character." in errors

def test_short_last_name(client):
    errors = validate_user_details("John", "S", "jsmith@testing.com", user_id=None)
    assert "Surname must be greater than 1 character." in errors