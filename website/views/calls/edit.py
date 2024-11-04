from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from ...models import Call
import re
from .. import views
from ... import db  

#Code to edit call
@views.route('/edit-call/<int:id>', methods=['GET', 'POST'])

@login_required
def edit_call(id):
    
    call_to_edit = Call.query.get_or_404(id)
    
    if request.method == 'POST':
        # Get form data
        customer_name = request.form['customer_name']
        account_number = request.form['account_number']
        postcode = request.form['postcode'].upper()
        reason_called = request.form['reason_called']

        # Validation
        errors = validate_call_data(customer_name, account_number, postcode, reason_called)

        if errors:
            # Flash error messages if validation fails
            for error in errors:
                flash(error, "error")
            # Render the edit template again with the current data
            return render_template('calls/edit.html', call_to_edit=call_to_edit, user=current_user)

        #if no errors then the data will be updated
        call_to_edit.customer.name = customer_name
        call_to_edit.customer.account_number = account_number
        call_to_edit.customer.postcode = postcode
        call_to_edit.reason_called = reason_called        

        db.session.commit()
        flash("Call record updated successfully!", "success")
        return redirect(url_for('views.view_calls'))  # Redirects to the view calls page

    return render_template('calls/edit.html', call_to_edit=call_to_edit, user=current_user)

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