import re

# Function that validates user entry before changes made to db.
def validate_call_data(customer_name, account_number, postcode, reason_called):
    errors = []  # List to collect error messages

    if len(customer_name) < 3:
        errors.append("Customer name must be at least 3 characters long!")

    if len(account_number) < 9 or len(account_number) > 10:
        errors.append("Invalid Account Number! Account numbers can only be 9 or 10 digits long!")

    postcode_error = validate_postcode(postcode)
    if postcode_error:
        errors.append(postcode_error)

    if reason_called not in ["Sale", "Withdrawal", "General Enquiry", "Complaint", "Online Support"]:
        errors.append('Invalid reason for call selected.')

    return errors

# Function to check postcode format
def validate_postcode(postcode):
    # Regex pattern - UK postcode
    pattern = r'^(GIR 0AA|[A-Z]{1,2}[0-9][0-9]?[A-Z]?\s?[0-9][A-Z]{2})$'
    if not re.match(pattern, postcode):
        return "Invalid Postcode!"
    return None
