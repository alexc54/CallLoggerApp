# views/__init__.py
from flask import Blueprint

views = Blueprint('views', __name__)

from .calls.home import *
from .calls.view import * 
from .calls.edit import *
from .calls.delete import *
from .calls.add import *

