from flask import render_template
from flask_login import login_required, current_user
from ...models import Call
from .. import views

#Code to display all call records 
@views.route('/calls', methods=['GET'])
@login_required
def view_calls():
    calls = Call.query.all()  
    return render_template('calls/view.html', calls=calls, user=current_user)
