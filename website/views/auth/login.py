from flask import Blueprint, render_template, request, flash, redirect, url_for
from ...models import User
from werkzeug.security import check_password_hash
from ... import db   
from flask_login import login_user, current_user
from . import auth



@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect password, try again.", category='error')
        else:
            flash("Email does not exist.", category='error')

    return render_template("auth/login.html", user=current_user)
