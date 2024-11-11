from flask import Blueprint, render_template, request, flash, redirect, url_for
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

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')           
        elif not re.match(r"^[A-Za-z\s]+$", first_name):
            flash("First name must contain only letters!", category='error')
        elif not re.match(r"^[A-Za-z\s]+$", last_name):
            flash("Surname must contain only letters!", category='error')       
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 6:
            flash('Password must be at least 6 characters.', category='error')        
        else:         
            #if passes validation then the user will be created
            new_user = User(email=email, first_name=first_name, last_name=last_name,password=generate_password_hash(password1, method='pbkdf2:sha256'),
                is_admin=is_admin)            

            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account has been created!", category='success')

            return redirect(url_for('views.home'))
    return render_template("auth/register.html", user=current_user)