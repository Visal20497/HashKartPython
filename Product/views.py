from flask import make_response, render_template, request, flash
from Product import product_bp
from Product.models import db, Product
from utils.jwt import login_required


@product_bp.route("/create-product", methods=['GET', 'POST'])
@login_required
def products():
    token = request.cookies.get('auth_token')
    if request.method == "POST":
        token=request.cookies.get('auth_token')

        name = request.form['name']
        brand = request.form.get('brand').strip().lower()
        category = request.form['category']
        price = request.form['price']
        description = request.form['description']
        image_url =request.form['image_url']
        

        new_product = Product(name=name, brand=brand, category=category,
                              price=price, description=description, image_url=image_url)
        db.session.add(new_product)
        db.session.commit()
        products = Product.query.all()
        flash("you add a new product !", "success")
        return render_template('add-Products.html', products=products,token=token), 201

    elif request.method == 'GET':
        products = Product.query.all()
    return render_template('add-Products.html', products=products,token=token), 200


@product_bp.route('/', methods=["GET"])
@login_required
def homePage():
    token = request.cookies.get('auth_token')
    if request.method == "GET":
        products = Product.query.all()
        categories = db.session.query(Product.category.distinct()).all()
        product_categories = [category[0] for category in categories]
        brands = db.session.query(Product.brand.distinct()).all()
        product_brands = [brand[0] for brand in brands]
    flash("get all the  product !", "success")
    response=make_response(render_template('home.html',token=token, products=products, product_categories=product_categories, product_brands=product_brands), 200)
    return response,200


@product_bp.route("/filter-product", methods=['GET', 'POST'])
@login_required
def filterProducts():
    token = request.cookies.get('auth_token')
    if request.method == "POST":
        sort = request.form.get('sort')
        brand = request.form.get('brand')
        category = request.form.get('category')

        categories = db.session.query(Product.category.distinct()).all()
        product_categories = [category[0] for category in categories]
        brands = db.session.query(Product.brand.distinct()).all()
        product_brands = [brand[0] for brand in brands]

        products = Product.query

        if sort is not None and len(sort.strip()) > 0:
            sort_field = sort.split("-")
            sort_by = sort_field[0]
            sort_order = sort_field[1]
            if sort_order == 'desc':
                products = products.order_by(
                    getattr(Product, sort_by).desc()).all()
            else:
                products = products.order_by(
                    getattr(Product, sort_by).asc()).all()
            return render_template('home.html',token=token, products=products, product_categories=product_categories, product_brands=product_brands), 201

        if brand is not None:
            products = products.filter_by(brand=brand).all()
            return render_template('home.html',token=token, products=products, product_categories=product_categories, product_brands=product_brands), 201

        if category is not None:
            products = products.filter_by(category=category).all()
            return render_template('home.html',token=token, products=products, product_categories=product_categories, product_brands=product_brands), 201

        products = products.all()
    return render_template('home.html',token=token, products=products, product_categories=product_categories, product_brands=product_brands), 201



