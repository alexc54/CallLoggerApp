from flask import render_template, request, flash, redirect, url_for, session
from ...models import User
from werkzeug.security import check_password_hash
from flask_login import login_user, current_user
from datetime import datetime, timedelta
from . import auth

@auth.route('/login', methods=['GET', 'POST'])
def login():
    #Amount of times user can enter incorrect password before being timed out
    MAX_LOGIN_ATTEMPTS = 3
    #Amount of time user will be locked out for
    LOCKOUT_TIME = timedelta(minutes=2)
    LOCKOUT_MINUTES = int(LOCKOUT_TIME.total_seconds() // 60)
    
    if request.method == 'POST':
        #Gets the email and password entered by the user
        email = request.form.get('email')
        password = request.form.get('password')
                
        #Track login attempts
        attempts = session.get('login_attempts', 0)
        lockout_until = session.get('lockout_until')

        if lockout_until:
            lockout_until = datetime.fromisoformat(lockout_until)
            if datetime.now() < lockout_until:
                remaining = (lockout_until - datetime.now()).seconds // 60 + 1
                flash(f"Too many failed attempts. Please wait {remaining} minutes and try again!.", category='error')
                return render_template("auth/login.html", user=current_user)
            else:
                session.pop('lockout_until')  #Lockout time expired
                session['login_attempts'] = 0
        
        #Checks the database to see if email exists
        user = User.query.filter_by(email=email).first()
        if user:
#Checks if the password entered matches the hashed password stored on the database, if so, user is logged in, success message appears and user taken to homepage
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category='success')
                login_user(user, remember=True)
                session.pop('login_attempts', None)  # Resets attempts when user logs in successful
                return redirect(url_for('views.home'))
            else:
            #If password entered is incorrect then this code tracks amount of time incorrectly entered
                attempts += 1
                session['login_attempts'] = attempts
                if attempts >= MAX_LOGIN_ATTEMPTS:
                    session['lockout_until'] = (datetime.now() + LOCKOUT_TIME).isoformat()                    
                    flash(f"Too many failed attempts. Please wait {LOCKOUT_MINUTES} minutes before trying again!", category='error')
                    
                else:
                    flash("Invalid email or password!", category='error')
                    remaining_attempts = MAX_LOGIN_ATTEMPTS - attempts
                    if remaining_attempts > 0:
                        flash(f"You have {remaining_attempts} login attempt(s) before being timed out for {LOCKOUT_MINUTES} minutes!", category='error')
                
        #If the email does not exist in the database, the below error appears to the user
        else:
         flash("Invalid email or password!", category='error')

    return render_template("auth/login.html", user=current_user)

