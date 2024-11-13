import re

# Function that validates user entry before changes made to db.
def validate_call_data(customer_name, account_number, postcode, reason_called=None):
    errors = []  # List to collect error messages

    if len(customer_name) < 3:
        errors.append("Customer name must be at least 3 characters long!")
    elif not re.match(r"^[A-Za-z\s]+$", customer_name):
        errors.append("Customer name must contain only letters and spaces!")

    if not account_number.isdigit() or not (9 <= len(account_number) <= 10):
        errors.append("Invalid Account Number! Account numbers can only be 9 or 10 digits long!")

    postcode_error = validate_postcode(postcode)
    if postcode_error:
        errors.append(postcode_error)

    # Only validate reason_called if it is provided
    if reason_called is not None:
        if reason_called not in ["Sale", "Withdrawal", "General Enquiry", "Complaint", "Online Support"]:
            errors.append('Invalid reason for call selected.')

    return errors

def validate_postcode(postcode):
    # Enhanced regex pattern for UK postcodes
    pattern = re.compile(
        r"^(GIR 0AA|"
        r"((([A-PR-UWYZ][0-9]{1,2})|"
        r"(([A-PR-UWYZ][A-HK-Y][0-9]{1,2})|"
        r"(([A-PR-UWYZ][0-9][A-HJKSTUW])|"
        r"([A-PR-UWYZ][A-HK-Y][0-9][ABEHMNPRVWXY]))))"
        r"\s?[0-9][ABD-HJLNP-UW-Z]{2}))$",
        re.IGNORECASE
    )

    # Check postcode against pattern
    if not pattern.match(postcode.strip()):
        return "Invalid Postcode!"
    return None