from flask import render_template, request, redirect, url_for, flash
from Cart import cart_bp
from Cart.models import db, Cart
from Product.models import Product
from utils.jwt import login_required


@cart_bp.route('/add-to-cart',methods=["GET","POST"])
@login_required
def AddToCart():
    token = request.cookies.get('auth_token')
    if request.method=="POST":
        product_id = request.form.get('product_id')
        cart = Cart.query.filter_by(product_id=product_id).first()
        if cart is None:
            cart = Cart(product_id=product_id, quantity=1)
        else:
            cart.quantity += 1
        db.session.add(cart)
        db.session.commit()
        
    flash("Product added to cart!", "success")
    return redirect(url_for("cart_bp.CartPage")), 301


@cart_bp.route('/remove-from-cart',methods=["POST"])
@login_required
def removeFromCart():
    if request.method=="POST":
        product_id = request.form.get('product_id')
        cart = Cart.query.filter_by(product_id=product_id).first()
        print(cart)
        if cart is not None and cart.quantity == 1:
            db.session.query(Cart).filter_by(product_id=product_id).delete()
        elif cart is not None and cart.quantity > 1:
            cart.quantity -= 1
        else:
            return "Exception"
        db.session.add(cart)
        db.session.commit()
    flash("Product removed from cart!", "success")
    return redirect(url_for("cart_bp.CartPage")), 301


@cart_bp.route('/cart', methods=["POST","GET"])
@login_required
def CartPage():
    token = request.cookies.get('auth_token')
    if request.method=="GET":
        carts = db.session.query(Product.id, Product.name, Product.category, Product.brand, Product.price, Product.image_url, Cart.quantity).join(Product, Cart.product_id == Product.id).all()
        total_amount = 0
        for product in carts:
            total_amount = total_amount + (product.price * product.quantity)
    return render_template('cart.html',token=token,carts=carts, total_amount=total_amount)