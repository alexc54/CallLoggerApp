from flask import render_template, request, flash, redirect, url_for
from ...models import User
from werkzeug.security import check_password_hash
from flask_login import login_user, current_user
from . import auth

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #Gets the email and password entered by the user
        email = request.form.get('email')
        password = request.form.get('password')
        #Checks the database to see if email exists
        user = User.query.filter_by(email=email).first()
        if user:
#Checks if the password entered matches the hashed password stored on the database, if so, user is logged in, success message appears and user taken to homepage
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect password, please try again!", category='error')
        #If the email does not exist in the database, the below error appears to the user
        else:
            flash("Email does not exist!", category='error')

    return render_template("auth/login.html", user=current_user)