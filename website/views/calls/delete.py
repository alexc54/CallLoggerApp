from flask import flash, redirect, url_for
from flask_login import login_required
from ...models import Call
from .. import views
from ... import db  

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
