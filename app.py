from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///HashKart.db'
    app.config["SECRET_KEY"] = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    db.init_app(app)
    bcrypt.init_app(app)

    from User.views import user_bp
    app.register_blueprint(user_bp)

    from Product.views import product_bp
    app.register_blueprint(product_bp)

    from Cart.views import cart_bp
    app.register_blueprint(cart_bp)

    from Payment.views import payment_bp
    app.register_blueprint(payment_bp)
    

    return app
