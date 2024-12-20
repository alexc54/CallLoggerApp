from flask_login import UserMixin
from sqlalchemy.orm import relationship
from .. import db  

# User database (Employees)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(20))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    #creates one-to-many relationship between User and Call (one user(employee) can have multiple calls)
    calls_handled = db.relationship('Call', back_populates='user')  