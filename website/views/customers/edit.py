from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from ...models import Customer
from .. import views
from ... import db  
from ..calls.validation import validate_call_data

#Code to edit call
@views.route('/edit-customer/<int:id>', methods=['GET', 'POST'])

@login_required
def edit_customer(id):
    
    #Checks the customer database to see if the customer exits
    customer_to_edit = Customer.query.get_or_404(id)
    
    if request.method == 'POST':
        #If customer exists then this gets the form data
        first_name = request.form['customer_first_name']
        last_name = request.form['customer_last_name']
        account_number = request.form['account_number']
        postcode = request.form['postcode'].upper()
       
        #Validation
        errors = validate_call_data(first_name, last_name, account_number, postcode)
        
          #Checks if customer already exists but with a different account number.
        existing_customer = Customer.query.filter(
            Customer.first_name.ilike(first_name.strip()), #Ignores case type and whitespace
            Customer.last_name.ilike(last_name.strip()),
            Customer.postcode.ilike(postcode.strip()),
            Customer.account_number != account_number,  #Checks if account numbers are different
            Customer.id != customer_to_edit.id 
        ).first()
        
        
        if existing_customer:
            errors.append("Customer with the same details already exists with a different account number!")  
           
        #Checks if account_number already in use by another customer.
        existing_account_number = Customer.query.filter_by(account_number=account_number).first()
        if existing_account_number and existing_account_number.id != customer_to_edit.id:
            errors.append("Account number already in use by another customer!")
           
        if errors:
            #Error messages if validation fails
            for error in errors:
                flash(error, "error")
            #Render the edit template again with the current data
            return render_template('customers/edit.html', customer_to_edit=customer_to_edit, user=current_user)

        #if no errors then the customer data will be updated
        customer_to_edit.first_name = first_name
        customer_to_edit.last_name = last_name
        customer_to_edit.account_number = account_number
        customer_to_edit.postcode = postcode
             
        #Saves the changes to the database, shows success message to user and the view calls page loads
        db.session.commit()
        flash("Customer updated successfully!", "success")
        return redirect(url_for('views.view_customers'))  # Redirects to the view calls page

    return render_template('customers/edit.html', customer_to_edit=customer_to_edit, user=current_user)