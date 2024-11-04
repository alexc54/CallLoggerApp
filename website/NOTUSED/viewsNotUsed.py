from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from . import db
from .models import Call, Customer
import re

views = Blueprint('views', __name__)

#Display home page
@views.route('/', methods=['GET'])
@login_required
def home():
    return render_template('home.html', user=current_user)

#Code to display all call records 
@views.route('/calls', methods=['GET'])
@login_required
def view_calls():
    calls = Call.query.all()  
    return render_template('view_call_log.html', calls=calls, user=current_user)

'''
# Code to insert call
@views.route('/add-call', methods=['GET', 'POST'])
@login_required
def add_call():
    if request.method == 'POST':
        customer_name = request.form.get('customer_name')
        account_number = request.form.get('account_number')
        postcode = request.form.get('postcode')
        reason_called = request.form.get('reason_called')

        # Validation 
        errors = validate_call_data(customer_name, account_number, postcode, reason_called)
        # If there are any errors, flash the messages and re-render the form
        if errors:
            for error in errors:
                flash(error, category='error')
            return render_template('add_call.html', user=current_user)  # Render the form template again

        # If no errors, add to database
        new_call = Call(
            customer_name=customer_name,
            account_number=account_number,
            postcode=postcode,
            reason_called=reason_called,
            user_id=current_user.id  # Associate the customer with the current user
        )        
        # commit record to db
        db.session.add(new_call)
        db.session.commit()

        flash("Call added successfully!", category='success')
        return redirect(url_for('views.view_calls'))  # Redirect to the customers list once customer has been added

    return render_template('add_call.html', user=current_user) 
'''


@views.route('/add-call', methods=['GET', 'POST'])
@login_required
def add_call():
    if request.method == 'POST':
        # Get data from the form
        name = request.form.get('customer_name')
        account_number = request.form.get('account_number')
        postcode = request.form.get('postcode')
        reason_called = request.form.get('reason_called')

        # Validation
        errors = validate_call_data(name, account_number, postcode, reason_called)
        if errors:
            for error in errors:
                flash(error, category='error')
            return render_template('add_call.html', user=current_user)

        # Check if customer exists; if not, create a new one
        customer = Customer.query.filter_by(account_number=account_number).first()
        if not customer:
            customer = Customer(name=name, account_number=account_number, postcode=postcode)
            db.session.add(customer)
            db.session.commit()  # Commit to save the new customer

        # Create the call with the associated user and customer
        new_call = Call(
            reason_called=reason_called,
            user_id=current_user.id,    # Associate the call with the current user
            customer_id=customer.id      # Associate the call with the found or newly created customer
        )
        db.session.add(new_call)
        db.session.commit()

        flash("Call added successfully!", category='success')
        return redirect(url_for('views.view_calls'))

    return render_template('add_call.html', user=current_user)


#Code to delete call
@views.route('/delete-call/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    call_to_delete = Call.query.get_or_404(id)
    try:
    #Code that runs when call has been deleted successfully
        db.session.delete(call_to_delete)
        db.session.commit()
        flash("Call has been deleted!", category='success')        
        return redirect(url_for('views.view_calls'))
    #If there is an error then the below code runs 
    except:
        flash("There was an error when attempting to delete the call!", category='error')
        return redirect(url_for('views.view_calls'))

#Code to edit call
@views.route('/edit-call/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_call(id):
    call_to_edit = Call.query.get_or_404(id)
    
    if request.method == 'POST':
        # Get form data
        customer_name = request.form['customer_name']
        account_number = request.form['account_number']
        postcode = request.form['postcode']
        reason_called = request.form['reason_called']

        # Validation
        errors = validate_call_data(customer_name, account_number, postcode, reason_called)

        if errors:
            # Flash error messages if validation fails
            for error in errors:
                flash(error, "error")
            # Render the edit template again with the current data
            return render_template('edit_call.html', call_to_edit=call_to_edit, user=current_user)

        #if no errors then the data will be updated
        call_to_edit.customer.name = customer_name
        call_to_edit.customer.account_number = account_number
        call_to_edit.customer.postcode = postcode
        call_to_edit.reason_called = reason_called        

        db.session.commit()
        flash("Call record updated successfully!", "success")
        return redirect(url_for('views.view_calls'))  # Redirects to the view calls page

    return render_template('edit_call.html', call_to_edit=call_to_edit, user=current_user)

#Function that validates user entry before changes made to db.
def validate_call_data(customer_name, account_number, postcode, reason_called):
    errors = []  # List to collect error messages
    
    if len(customer_name) < 3:
        errors.append("Customer name must be at least 3 characters long!")
    
    if len(account_number) < 9 or len(account_number) > 10:
        errors.append("Invalid Account Number!")        
        
    postcode_error = validate_postcode(postcode)
    if postcode_error:
        errors.append(postcode_error)

    if reason_called not in ["Sale", "Withdrawal", "General Enquiry", "Complaint", "Online Support"]:
        errors.append('Invalid reason for call selected.')

    return errors

#Function that will check postcode has been entered correctly
def validate_postcode(postcode):
    # Regex pattern for UK postcode
    pattern = r'^(GIR 0AA|[A-Z]{1,2}[0-9][0-9]?[A-Z]?\s?[0-9][A-Z]{2})$'
    if not re.match(pattern, postcode):
        return "Invalid Postcode!"
    return None 