from flask import Blueprint

views = Blueprint('views', __name__)

from ..customers.view import *
from ..customers.edit import *
