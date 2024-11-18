from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from ...models import Call
from .. import views
from ... import db  
from .validation import validate_call_data

#Code to edit call
@views.route('/edit-call/<int:id>', methods=['GET', 'POST'])

@login_required
def edit_call(id):
    #Checks the call database to see if the call exits
    call_to_edit = Call.query.get_or_404(id)
    
    if request.method == 'POST':
        #If call does exist then this gets the form data
        customer_first_name = request.form['customer_first_name']
        customer_last_name = request.form['customer_last_name']
        account_number = request.form['account_number']
        postcode = request.form['postcode'].upper()
        reason_called = request.form['reason_called']

        #Validation
        errors = validate_call_data(customer_first_name,customer_last_name, account_number, postcode, reason_called)

        if errors:
            #Error messages if validation fails
            for error in errors:
                flash(error, "error")
            #Render the edit template again with the current data
            return render_template('calls/edit.html', call_to_edit=call_to_edit, user=current_user)

        #If no errors then the call will be updated with new input
        call_to_edit.customer.first_name = customer_first_name
        call_to_edit.customer.last_name = customer_last_name
        call_to_edit.customer.account_number = account_number
        call_to_edit.customer.postcode = postcode
        call_to_edit.reason_called = reason_called        

        #Saves the changes to the database, shows success message to user and the view calls page loads
        db.session.commit()
        flash("Call record updated successfully!", "success")
        return redirect(url_for('views.view_calls')) 

    return render_template('calls/edit.html', call_to_edit=call_to_edit, user=current_user)