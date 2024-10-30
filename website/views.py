from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from . import db
from .models import Customer

views = Blueprint('views', __name__)

#Display home page
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user)

#Code to display all call records 
@views.route('/calls', methods=['GET'])
@login_required
def view_calls():
    customers = Customer.query.all()  
    return render_template('view_call_log.html', customers=customers, user=current_user)

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
        new_customer = Customer(
            customer_name=customer_name,
            account_number=account_number,
            postcode=postcode,
            reason_called=reason_called,
            user_id=current_user.id  # Associate the customer with the current user
        )
        
        # commit record to db
        db.session.add(new_customer)
        db.session.commit()

        flash("Customer added successfully!", category='success')
        return redirect(url_for('views.view_calls'))  # Redirect to the customers list once customer has been added

    return render_template('add_call.html', user=current_user) 


#Function that validates user entry before being inserted into the database
def validate_call_data(customer_name, account_number, postcode, reason_called):
    errors = []  # List to collect error messages
    
    if len(customer_name) < 3:
        errors.append("Customer name must be at least 3 characters long!")
    
    if len(account_number) < 9 or len(account_number) > 10:
        errors.append("Invalid Account Number!")   
        
    if len(postcode) < 5 or len(postcode) > 7:
        errors.append("Invalid Postcode!")        

    if reason_called not in ["Sale", "Withdrawal", "General Enquiry", "Complaint", "Online Support"]:
        errors.append('Invalid reason for call selected.')

    return errors

'''
#Code to insert call
@views.route('/add-call', methods=['GET', 'POST'])
@login_required
def add_call():
    if request.method == 'POST':
        customer_name = request.form.get('customer_name')
        account_number = request.form.get('account_number')
        postcode = request.form.get('postcode')
        reason_called = request.form.get('reason_called')

 # Validation checks
        if not customer_name:
            flash('Customer name is required.', category='error')
        elif len(customer_name) < 3:
            flash('Customer name must be at least 3 characters long.', category='error')
        elif not account_number:
            flash('Account number is required.', category='error')
        elif len(account_number) < 8:
            flash('Invalid Account Number!', category='error')
        elif not postcode:
            flash('Postcode is required.', category='error')
        elif len(postcode) < 3:
            flash('Postcode must be at least 3 characters long.', category='error')
        elif reason_called not in ["Sale", "Withdrawal", "General Enquiry", "Complaint", "Online Support"]:
            flash('Invalid reason for call selected.', category='error')
        else:       # add to database
            new_customer = Customer(
            customer_name=customer_name,
            account_number=account_number,
            postcode=postcode,
            reason_called=reason_called,
            user_id=current_user.id  # Associate the customer with the current user
        )
        # Add the new call and committing this to the database
        db.session.add(new_customer)
        db.session.commit()

        flash('Customer added successfully!', category='success')
        return redirect(url_for('views.view_calls'))  # Redirect to the customers list

    return render_template('add_call.html', user=current_user)  # Render the form template
'''

#Code to delete call
@views.route('/delete-call/<int:id>', methods=['GET', 'POST'])
def delete(id):
    user_to_delete = Customer.query.get_or_404(id)
    try:
    #Code that runs when call has been deleted successfully
        db.session.delete(user_to_delete)
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
    user_to_edit = Customer.query.get_or_404(id)
    
    if request.method == 'POST':        
        user_to_edit.customer_name = request.form['customer_name']
        user_to_edit.account_number = request.form['account_number']
        user_to_edit.postcode = request.form['postcode']
        user_to_edit.reason_called = request.form['reason_called']        

        db.session.commit()
        flash("Call record updated successfully!", "success")
        return redirect(url_for('views.view_calls'))  #Redirects user back to all calls once editing has been saved.

    return render_template('edit_call.html', user_to_edit=user_to_edit, user=current_user)


