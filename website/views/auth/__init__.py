from flask import Blueprint

auth = Blueprint('auth', __name__)

# Import routes
from .register import *
from .login import *
from .logout import *
