
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
    
    response = client.get('/users')
   #Checks that user is redirected to login page and no access given
    assert response.status_code == 302 
    response = client.get('/login')  
    assert b'Call Logger App' in response.data
