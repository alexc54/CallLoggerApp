from flask import render_template, request
from flask_login import login_required, current_user
from ...models import Call
from .. import views

#Code to display all call records 
@views.route('/calls', methods=['GET'])
@login_required
def view_calls():
    
     #Get the search query from variable called search_for_customer
     search = request.args.get('call_search')  

    #Checks if searchbar has anything input
     if search:
    #If something has been input below will check customer name, account number and postcode for a match
        calls = Call.query.filter(
            (Call.id.ilike(f'%{search}%')) | 
            (Call.reason_called.ilike(f'%{search}%'))).all() 
     else:
        #If nothing entered in the searchbar , all customers will display
        calls = Call.query.all()
        
     return render_template('calls/view.html', calls=calls, user=current_user)

    

