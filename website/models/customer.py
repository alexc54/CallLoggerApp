from sqlalchemy.orm import relationship
from .. import db  

#Customer database
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    account_number = db.Column(db.Integer, unique=True)
    postcode = db.Column(db.String(8))

    #creates one-to-many relationship between customer and calls (one Customer can have multiple Calls)
    calls = relationship('Call', back_populates='customer') 
