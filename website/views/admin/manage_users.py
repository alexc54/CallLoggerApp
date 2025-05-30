from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from website.models import User
from website import db
from website.views.auth.user_validation import validate_user_details

admin = Blueprint('admin', __name__)

#Function to give user admin access
@admin.route('/give_admin_access/<int:user_id>', methods=['GET'])
@login_required
def give_admin_access(user_id):
    #Check if current user is an admin as only admins should be able to add permissions
    if not current_user.is_admin:
        flash('You are not authorised to perform this action.', 'error')
        return redirect(url_for('admin.users'))
    
    #Check to see if user is already an admin
    user_to_admin = User.query.get_or_404(user_id)
    if user_to_admin.is_admin:
        flash('This user is already an admin.', 'error')
    else:
        #Changes user role to admin and saves to database
        user_to_admin.is_admin = True
        db.session.commit()
        flash(f'{user_to_admin.first_name} {user_to_admin.last_name} has been given admin access!', 'success')

    return redirect(url_for('admin.users'))

@admin.route('/remove_admin_access/<int:user_id>', methods=['GET'])
@login_required

#Function to remove admin access from user
def remove_admin_access(user_id):
    #Check if current user is an admin as only admins should be able to remove permissions
    if not current_user.is_admin:
        flash('Only admins can remove permissions!', 'error')
        return redirect(url_for('admin.users'))
    
    #Check to see if user is already not admin
    user_to_non_admin = User.query.get_or_404(user_id)
    if not user_to_non_admin.is_admin:
        flash('This user is not an admin.', 'error')
    #Stops users accidently removing own access    
    elif user_to_non_admin.id == current_user.id:
        flash('You cannot remove admin access to yourself!', 'error')
    else:
        #Removes admin access and saves to database
        user_to_non_admin.is_admin = False
        db.session.commit()
        flash(f'{user_to_non_admin.first_name} {user_to_non_admin.last_name} no longer has admin access!', 'success')

    return redirect(url_for('admin.users'))

#Function that dislays all users onto table
@admin.route('/users', methods=['GET'])
@login_required
def users():
    #if user is not an admin user, will display error and take them to homepage
    if not current_user.is_admin:
        flash('Please login as an admin to view this page!', 'danger')
        return redirect(url_for('views.home'))
    
     #Get the search query from variable called search_for_customer
    search = request.args.get('employee_search')  

    #Checks if searchbar has anything input
    if search:
    #If something has been input below will check customer name, account number and postcode for a match
        users = User.query.filter(
            (User.first_name.ilike(f'%{search}%')) | 
            (User.last_name.ilike(f'%{search}%')) | 
            (User.email.ilike(f'%{search}%'))).all() 
    else:
        #If nothing entered in the searchbar , all customers will display    
        
        users = User.query.all()
    return render_template('admin/users.html', users=users)


# Route to render the edit form
@admin.route('/edit_user/<int:user_id>', methods=['GET'])
@login_required
def edit_user(user_id):
    if not current_user.is_admin:
        flash('Only admins can edit user details!', 'error')
        return redirect(url_for('admin.users'))

    user = User.query.get_or_404(user_id)
    return render_template('admin/edit_user.html', user=user)


# Route to handle the edit form submission
@admin.route('/edit_user/<int:user_id>', methods=['POST'])
@login_required
def update_user(user_id):
    if not current_user.is_admin:
        flash('You are not authorised to perform this action.', 'error')
        return redirect(url_for('admin.users'))

    user = User.query.get_or_404(user_id)

    # Get data from form
    new_first_name = request.form.get('first_name')
    new_last_name = request.form.get('last_name')
    new_email = request.form.get('email')
    
    
    # Reuse the validation logic
    errors = validate_user_details(new_first_name, new_last_name, new_email, user_id=user.id)

    if errors:
        for error in errors:
            flash(error, category='error')
        return redirect(url_for('admin.edit_user', user_id=user.id))

    # Update user fields
    user.first_name = new_first_name
    user.last_name = new_last_name
    user.email = new_email

    db.session.commit()
    flash(f'{user.first_name} {user.last_name}\'s details have been updated.', 'success')

    return redirect(url_for('admin.users'))
