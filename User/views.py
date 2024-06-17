from flask import redirect, render_template, request, flash, make_response, url_for
from Product.models import Product
from User import user_bp
from User.models import db, User
from app import bcrypt
from utils.jwt import encode_token


def generate_password_hash(password):
    return bcrypt.generate_password_hash(password=password).decode("utf-8")

def check_password_hash(userPassword,password):
    return bcrypt.check_password_hash(userPassword,password)





@user_bp.route("/register", methods=['GET', 'POST'])
def register():
    token = request.cookies.get('auth_token')
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
       
        # check if email already exists
        if User.query.filter_by(email=email).first():
            return render_template('register_view.html', error='Email or mobile no already exists'), 404

      # create new user
        new_user = User(name=username, email=email,
                        password=generate_password_hash(password), phone=phone)
        db.session.add(new_user)
        db.session.commit()
        flash("your account has been created!", "success")
        return render_template('login_view.html',token=token), 201

    return render_template('register_view.html',token=token), 404


@user_bp.route("/login", methods=['GET', 'POST'])
def login():
    token = request.cookies.get('auth_token')
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            token = encode_token(user)
            flash("You have been logged in!", "success")
            products = Product.query.all()
            categories = db.session.query(Product.category.distinct()).all()
            product_categories = [category[0] for category in categories]
            brands = db.session.query(Product.brand.distinct()).all()
            product_brands = [brand[0] for brand in brands]
            response = make_response(render_template('home.html',token=token,products=products, product_categories=product_categories, product_brands=product_brands),200)
            response.set_cookie('auth_token', token) 
            return response,200
        else:
            flash("Either email or password is incorrect!", "error"), 500
            return render_template('login_view.html',token=token)

    return render_template('login_view.html',token=token), 500




@user_bp.route('/logout', methods=["GET"])
def logout():
    token = request.cookies.get('auth_token')
    if request.method == "GET":
        response = make_response(redirect(url_for('user_bp.LoginPage')))
        response.set_cookie('auth_token', '', expires=0)
        flash("You have been logged out. Please clear the token on the client side.", "info")
        return response
    
@user_bp.route('/logoutPage',methods=["GET"])
def LoginPage():
    return render_template('login_view.html')