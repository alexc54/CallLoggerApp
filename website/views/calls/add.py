from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from ... import db
from ...models import Call, Customer
from ..import views
from .validation import validate_call_data

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
            return render_template('calls/add.html', user=current_user)

        # This will check if the customer exists on the customer DB; if not, it will add them
        customer = Customer.query.filter_by(account_number=account_number).first()
        if not customer:
            customer = Customer(name=name, account_number=account_number, postcode=postcode)
            db.session.add(customer)
            db.session.commit()  # Commit to save the new customer

        # Create the call with the associated user and customer
        new_call = Call(
            reason_called=reason_called,
            user_id=current_user.id,    # Link the call with the current user
            customer_id=customer.id      # Link the call with the new or existing customer
        )
        db.session.add(new_call)
        db.session.commit()

        flash("Call added successfully!", category='success')
        return redirect(url_for('views.view_calls'))

    return render_template('calls/add.html', user=current_user)

