from flask import Blueprint

payment_bp = Blueprint('payment_bp', __name__,
                        template_folder='templates')