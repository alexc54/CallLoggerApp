from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .. import db  


#Call database
class Call(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reason_called = db.Column(db.String(150))
    date = db.Column(db.DateTime(timezone=True), default=func.now())    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name="fk_call_user_id"))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id', name="fk_call_customer_id"))
    
    # Relationship to User (who handled the call)
    user = relationship('User', back_populates='calls_handled') 

    # Relationship to Customer (who the call is about)
    customer = relationship('Customer', back_populates='calls')