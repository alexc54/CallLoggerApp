import pytest
from website import create_app

#Create the app so tests can take place
@pytest.fixture
def client():
    app = create_app()  
    with app.app_context():  
        yield app.test_client()  

#Testing if Register and Login load correctly

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
    
#Register Page
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
    
    
#Authetication Tests
    
#Testing if users can login to the application   
def test_login_correct_credentials(client, test_user):
    response = client.post('/login', data={
        'email': 'testuser@example.com',
        'password': 'CorrectPassword123'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Logged in successfully!" in response.data
    assert b"User: Test User" in response.data  #Checks navbar displays name


    
    
#Testing authentication with incorrect details
def test_login_incorrect_credentials(client):
    response = client.post('/login', data={
        'email': 'wrong@example.com',
        'password': 'WrongPassword123'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Invalid email or password!" in response.data


    
#Testing users can logout    
def test_logout(client, test_user):
    # Step 1: Log in
    client.post('/login', data={
        'email': 'testuser@example.com',
        'password': 'CorrectPassword123'
    }, follow_redirects=True)

    #Logging out
    response = client.get('/logout', follow_redirects=True)

    #Check user is logged out
    assert response.status_code == 200
    assert b"Sign in" in response.data          
    
    

#Testing users can access pages when logged in    
def test_access_pages(client, test_user):    
    #Logs user in using existing testing account credentials 
    client.post('/login', data={
        'email': 'testuser@example.com',
        'password': 'CorrectPassword123'
    }, follow_redirects=True)  
    #Test user can access all pages that require login
    response = client.get('/customers')  
    assert response.status_code == 200  #Checks page has loaded correctly
    assert b'Customer Records' in response.data  #Checks that Customer Records is on the loaded page
    #Below checks table displays
    assert b'<table' in response.data 
    
    response = client.get('/edit-customer/1')
    assert response.status_code == 200  
    assert b'Edit Customer Details' in response.data  
    #Below checks if a form displays 
    assert b'<form' in response.data 
    
    response = client.get('/add-call')  
    assert response.status_code == 200  
    assert b'Log New Call' in response.data  
    #Below checks if a form displays 
    assert b'<form' in response.data 
    
    response = client.get('/calls')
    assert response.status_code == 200  
    assert b'Call Logger Record' in response.data  
    #Below checks table displays
    assert b'<table' in response.data 
    
    response = client.get('/edit-call/1')
    assert response.status_code == 200  
    assert b'Edit Call Reason' in response.data 
    #Below checks if a form displays 
    assert b'<form' in response.data 
    
    
    
#Testing users cannot access webpages with customer data without logging in first    
def test_user_cannot_access_sensitive_pages_without_login(client):
    #GET request to access the customers page     
    response = client.get('/customers')  
   #Checks that user is redirected to login page and no access given
    assert response.status_code == 302 
    response = client.get('/login')  
    assert b'Call Logger App' in response.data
    
    response = client.get('/edit-customer/1')
   #Checks that user is redirected to login page and no access given
    assert response.status_code == 302 
    response = client.get('/login')  
    assert b'Call Logger App' in response.data

    response = client.get('/add-call')  
   #Checks that user is redirected to login page and no access given
    assert response.status_code == 302 
    response = client.get('/login')  
    assert b'Call Logger App' in response.data

    response = client.get('/calls')
   #Checks that user is redirected to login page and no access given
    assert response.status_code == 302 
    response = client.get('/login')  
    assert b'Call Logger App' in response.data
 
    response = client.get('/edit-call/1')
   #Checks that user is redirected to login page and no access given
    assert response.status_code == 302 
    response = client.get('/login')  
    assert b'Call Logger App' in response.data
