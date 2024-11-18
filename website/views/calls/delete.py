from flask import flash, redirect, url_for
from flask_login import login_required
from ...models import Call
from .. import views
from ... import db  

#Code to delete call
@views.route('/delete-call/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    #Checks the call database to see if the call exists
    call_to_delete = Call.query.get_or_404(id)
    try:
    #If call exists then this code runs to delete the call and success message will appear
        db.session.delete(call_to_delete)
        db.session.commit()
        flash("Call has been deleted!", category='success')        
        return redirect(url_for('views.view_calls'))
    #If there is an error then error message appears
    except:
        flash("There was an error when attempting to delete the call!", category='error')
        return redirect(url_for('views.view_calls'))
