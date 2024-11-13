from flask import render_template, request, flash, redirect, url_for
from ...models import User
from werkzeug.security import generate_password_hash
from ... import db   
from flask_login import login_user, current_user
from . import auth
import re

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        is_admin = 'isAdmin' in request.form
        
        errors = []  # List to collect error messages

        user = User.query.filter_by(email=email).first()    
       
        if user:
            errors.append("Email already exists.")           
        if not re.match(r"^[A-Za-z\s]+$", first_name):
            errors.append("First name must contain only letters!")
        if not re.match(r"^[A-Za-z\s]+$", last_name):
            errors.append("Surname must contain only letters!")       
        if len(email) < 4:
            errors.append("Email must be greater than 3 characters.")
        if len(first_name) < 2:
            errors.append("First name must be greater than 1 character.")
        if len(last_name) < 2:
            errors.append("Surname must be greater than 1 character.")
        if password1 != password2:
            errors.append("Passwords don\'t match.")
        if len(password1) < 6: #Checks the password is greater than 6 characters long
            errors.append("Password must be at least 6 characters.")      
        if not re.search(r"\d", password1):  #Checks the password has atleast one digit
            errors.append("Password must contain at least one number.")  
        if not re.search(r"[A-Z]", password1):  #Checks the password has at least one uppercase letter
            errors.append("Password must contain at least one uppercase letter.")
         
        #Displays all the error messages on screen    
        for error in errors:
            flash(error, category='error')
            
        if not errors:        
            #if validation passed then the new user will be created
            new_user = User(email=email, first_name=first_name, last_name=last_name,password=generate_password_hash(password1, method='pbkdf2:sha256'),
                is_admin=is_admin)            

            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account has been created!", category='success')

            return redirect(url_for('views.home'))
    return render_template("auth/register.html", user=current_user)