from flask import render_template, request
from flask_login import login_required, current_user
from ...models import Customer
from .. import views

#Code to displays customer records 
@views.route('/customers', methods=['GET'])
@login_required
def view_customers():
   #Get the search query from variable called search_for_customer
     search = request.args.get('customer_search')  

    #Checks if searchbar has anything input
     if search:
    #If something has been input below will check customer name, account number and postcode for a match
        customers = Customer.query.filter(
            (Customer.first_name.ilike(f'%{search}%')) | 
            (Customer.last_name.ilike(f'%{search}%')) | 
            (Customer.account_number.ilike(f'%{search}%')) | 
            (Customer.postcode.ilike(f'%{search}%'))).all() 
        
     else:
        #If nothing entered in the searchbar , all customers will display
        customers = Customer.query.all()

    
     return render_template('customers/view.html', customers=customers, user=current_user)

