from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from ... import db
from ...models import Call, Customer
from ..import views
from .validation import validate_call_data

@views.route('/add-call', methods=['GET', 'POST'])
@login_required #Makes sure user is logged in
def add_call():
    if request.method == 'POST':
        # Get data that was inserted from the form
        first_name = request.form.get('customer_first_name')
        last_name = request.form.get('customer_last_name')
        account_number = request.form.get('account_number')
        postcode = request.form.get('postcode')
        reason_called = request.form.get('reason_called')

        #Validation method called
        errors = validate_call_data(first_name, last_name, account_number, postcode, reason_called)    
              
        #Checks if customer already exists but with a different account number.
        existing_customer = Customer.query.filter(
            Customer.first_name.ilike(first_name.strip()), #Ignores case type and whitespace
            Customer.last_name.ilike(last_name.strip()),
            Customer.postcode.ilike(postcode.strip()),
            Customer.account_number != account_number  #Checks if account numbers are different
        ).first()
        
        if existing_customer:
             errors.append("Customer with the same details already exists with a different account number!") 
        
         #Check if the customer exists on the customer DB - Will add them if not
        customer = Customer.query.filter_by(account_number=account_number).first()        
        if customer:
        #Check if the existing customer's name and postcode match the input data, code added so not case sensitive and whitespace ignored 
           if customer.first_name.replace(" ", "").lower() != first_name.replace(" ", "").lower() or \
            customer.last_name.replace(" ", "").lower() != last_name.replace(" ", "").lower() or \
            customer.postcode.replace(" ", "").lower() != postcode.replace(" ", "").lower():
        #If the customer details do not match what is already on record, flash an error and stop the call creation
                errors.append("The customer details do not match the records for this account number. \
                    Verify the account number or update the customer information on the customer records page.")   
      
        #If there are any errors, this will display on the screen using flash
        if errors:
            for error in errors:
                flash(error, category='error')
            return render_template('calls/add.html', user=current_user)         
       
        #If customer does not already exist then a new customer is created and added to the customer database
        if not customer:
            customer = Customer(first_name=first_name, last_name=last_name, account_number=account_number, postcode=postcode)
            db.session.add(customer)
            db.session.commit()  #Commit to save the new customer          

        #Create a new call with the current user and customer
        new_call = Call(
            reason_called=reason_called,
            user_id=current_user.id,  #Link the call with the current user
            customer_id=customer.id   #Link the call with the new or existing customer
        )
        db.session.add(new_call)
        db.session.commit()

        flash("Call added successfully!", category='success')
        return redirect(url_for('views.view_calls'))

    return render_template('calls/add.html', user=current_user)

