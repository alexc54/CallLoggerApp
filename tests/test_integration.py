    
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
    
    
