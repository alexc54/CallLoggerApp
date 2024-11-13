from flask import render_template
from flask_login import login_required, current_user
from ...models import Customer
from .. import views

#Code to display all customer records 
@views.route('/customers', methods=['GET'])
@login_required
def view_customers():
    customers = Customer.query.all()  
    return render_template('customers/view.html', customers=customers, user=current_user)

