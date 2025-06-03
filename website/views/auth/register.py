from flask import render_template, request, flash, redirect, url_for
from ...models import User
from werkzeug.security import generate_password_hash
from ... import db   
from flask_login import login_user, current_user
from . import auth
import re
from website.views.auth.user_validation import validate_user_details

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        #Gets all the data input by the user
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        is_admin = 'isAdmin' in request.form
        
        #errors = []  #List created, any errors that occur are added to this list and displayed when user submits


        errors = validate_user_details(first_name, last_name, email,user_id=None)
        
        
        
        #Checks both passwords input are the same
        if password1 != password2:
            errors.append("Passwords don\'t match.")
        #Checks password is greater than 6 characters long
        if len(password1) < 6: 
            errors.append("Password must be at least 6 characters.")  
        #Checks the password has atleast one digit    
        if not re.search(r"\d", password1): 
            errors.append("Password must contain at least one number.")  
        #Checks the password has at least one uppercase letter
        if not re.search(r"[A-Z]", password1):  
            errors.append("Password must contain at least one uppercase letter.")
         
        #Displays errors onto the screen
        for error in errors:
            flash(error, category='error')
            
        if not errors:        
        #if validation passed then a new user will be created and success message to confirm to user appears
            new_user = User(email=email, first_name=first_name, last_name=last_name,password=generate_password_hash(password1, method='pbkdf2:sha256'),
                is_admin=is_admin)            
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account has been created!", category='success')
        #User is then logged in automatically and taken to the homepage
            return redirect(url_for('views.home'))
    return render_template("auth/register.html", user=current_user)