from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from website.models import User
from website import db

admin = Blueprint('admin', __name__)


@admin.route('/give_admin_access/<int:user_id>', methods=['GET'])
@login_required
def give_admin_access(user_id):
    if not current_user.is_admin:
        flash('You are not authorised to perform this action.', 'error')
        return redirect(url_for('admin.users'))

    user_to_admin = User.query.get_or_404(user_id)

    if user_to_admin.is_admin:
        flash('This user is already an admin.', 'warning')
    else:
        user_to_admin.is_admin = True
        db.session.commit()
        flash(f'{user_to_admin.first_name} {user_to_admin.last_name} has been given admin access!', 'success')

    return redirect(url_for('admin.users'))

@admin.route('/remove_admin_access/<int:user_id>', methods=['GET'])
@login_required
def remove_admin_access(user_id):
    if not current_user.is_admin:
        flash('Only admins can remove permissions!', 'error')
        return redirect(url_for('admin.users'))

    user_to_non_admin = User.query.get_or_404(user_id)

    if not user_to_non_admin.is_admin:
        flash('This user is not an admin.', 'error')
    elif user_to_non_admin.id == current_user.id:
        flash('You cannot remove admin access to yourself!', 'error')
    else:
        user_to_non_admin.is_admin = False
        db.session.commit()
        flash(f'{user_to_non_admin.first_name} {user_to_non_admin.last_name} no longer has admin access!', 'success')

    return redirect(url_for('admin.users'))


@admin.route('/users', methods=['GET'])
@login_required
def users():
    if not current_user.is_admin:
        flash('Please login as an admin to view this page!', 'danger')
        return redirect(url_for('views.home'))

    users = User.query.all()
    return render_template('admin/users.html', users=users)
