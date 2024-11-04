from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

# User database (Employees)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(20))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    #creates one-to-many relationship between User and Call (One user(employee) can have multiple calls)
    calls_handled = db.relationship('Call', back_populates='user')  

#Call database
class Call(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reason_called = db.Column(db.String(100))
    date = db.Column(db.DateTime(timezone=True), default=func.now())    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name="fk_call_user_id"))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id', name="fk_call_customer_id"))
    
    # Relationship to User (who handled the call)
    user = relationship('User', back_populates='calls_handled') 

    # Relationship to Customer (who the call is about)
    customer = relationship('Customer', back_populates='calls')

#Customer database
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    account_number = db.Column(db.String(50), unique=True)
    postcode = db.Column(db.String(10))

    #creates one-to-many relationship between customer and calls (one Customer can have multiple Calls)
    calls = relationship('Call', back_populates='customer')  # This part is correct
