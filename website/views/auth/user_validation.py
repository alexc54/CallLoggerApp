import re
from website.models import User
from sqlalchemy import func

def validate_user_details(first_name, last_name, email, user_id):
    
    #Validation on users details and returns a list of error messages.
   
    
    errors = []

    lowercase_email = email.strip().lower()

    #Check for duplicate email, not including current users
    existing_user = User.query.filter(
        func.lower(User.email) == lowercase_email
    ).first()
    if existing_user and (user_id is None or existing_user.id != user_id):
        errors.append("Email already exists.")


    #Validation for users name and email format and length 
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

    return errors