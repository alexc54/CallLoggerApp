import re
from ...models import Customer

#Function that validates user entry before changes made to db.
def validate_call_data(customer_first_name, customer_last_name, account_number, postcode, reason_called=None):
    errors = []  #List to collect all errors

#Checks customer name is atleast 3 characters long and only contains letters and spaces(No numbers or special characters allowed)
    if len(customer_first_name) < 3:
        errors.append("Customer First Name must be at least 3 characters long!")
    if len(customer_last_name) < 3:
        errors.append("Customer Surname must be at least 3 characters long!")
    if not re.match(r"^[A-Za-z\s]+$", customer_first_name):
        errors.append("Customer First Name must contain only letters!")
    if not re.match(r"^[A-Za-z\s]+$", customer_last_name):
        errors.append("Customer Surname must contain only letters!")
#Checks account number is a number and is 9 or 10 digits long
    if not account_number.isdigit() or not (9 <= len(account_number) <= 10):
        errors.append("Invalid Account Number! Account numbers can only be 9 or 10 digits long!")

#Uses validate postcode function to check postcode is in the correct format
    postcode_error = validate_postcode(postcode)
    if postcode_error:
        errors.append(postcode_error)

    #Validate reason_called if it is provided
    if reason_called is not None:
        if reason_called not in ["Sale", "Withdrawal", "General Enquiry", "Complaint", "Online Support"]:
            errors.append('Invalid reason for call selected.')

#Displays the list of all the errors to the user if any
    return errors

def validate_postcode(postcode):
    #Pattern for UK postcodes to make sure a correct postcode was entered
    pattern = re.compile(
        r"^(GIR 0AA|"
        r"((([A-PR-UWYZ][0-9]{1,2})|"
        r"(([A-PR-UWYZ][A-HK-Y][0-9]{1,2})|"
        r"(([A-PR-UWYZ][0-9][A-HJKSTUW])|"
        r"([A-PR-UWYZ][A-HK-Y][0-9][ABEHMNPRVWXY]))))"
        r"\s?[0-9][ABD-HJLNP-UW-Z]{2}))$",
        re.IGNORECASE
    )
    #Check input postcode against pattern, error message will display if invalid
    if not pattern.match(postcode.strip()):
        return "Invalid Postcode!"
    return None


#Functions that checks if customer details entered already exists but with a different account number 
def check_existing_customer(first_name, last_name, postcode, account_number, current_customer_id=None):
       
    existing_customer = Customer.query.filter(
        Customer.first_name.ilike(first_name.strip()),  # Ignore case and whitespace
        Customer.last_name.ilike(last_name.strip()),
        Customer.postcode.ilike(postcode.strip()),
        Customer.account_number != account_number,  # Ensure the account number is different
        Customer.id != current_customer_id  # Exclude the current customer if provided
    ).first()

    if existing_customer:
        return "Customer with the same details already exists with a different account number!"
    return None