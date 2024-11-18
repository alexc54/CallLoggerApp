# views/home.py
from flask import render_template
from flask_login import login_required, current_user
from .. import views

#Loads the homepage 
@views.route('/', methods=['GET'])
@login_required
def home():
    return render_template('calls/home.html', user=current_user)
