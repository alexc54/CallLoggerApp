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
    
    customer_to_edit = Customer.query.get_or_404(id)
    
    if request.method == 'POST':
        # Get form data
        customer_name = request.form['customer_name']
        account_number = request.form['account_number']
        postcode = request.form['postcode'].upper()
       

        # Validation
        errors = validate_call_data(customer_name, account_number, postcode)

        if errors:
            # Flash error messages if validation fails
            for error in errors:
                flash(error, "error")
            # Render the edit template again with the current data
            return render_template('customers/edit.html', customer_to_edit=customer_to_edit, user=current_user)

        #if no errors then the data will be updated
        customer_to_edit.name = customer_name
        customer_to_edit.account_number = account_number
        customer_to_edit.postcode = postcode
             

        db.session.commit()
        flash("Customer updated successfully!", "success")
        return redirect(url_for('views.view_customers'))  # Redirects to the view calls page

    return render_template('customers/edit.html', customer_to_edit=customer_to_edit, user=current_user)