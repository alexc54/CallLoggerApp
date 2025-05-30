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
    
    