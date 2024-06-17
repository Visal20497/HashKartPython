from flask import jsonify, render_template, request, redirect
from Cart.models import Cart
from Payment import payment_bp
from Product.models import Product
from app import db
import stripe

from Payment.models import Payment ,db
from utils.jwt import login_required


domain_url = "http://127.0.0.1:5000/"
stripe.api_key = "sk_test_51PRIMmAgzzc5MvhghuNAAYVcNVLYQUxFDRlKwU4jl9XoP0aCQNAMq6qeTTXGEsBvYAW98h9AKL0bkejN2X2hzbFn00ZqDzJUXP"


@payment_bp.route("/create-checkout-session", methods=["POST", "GET"])
@login_required
def create_checkout_session():
    if request.method == "POST":
        carts = db.session.query(Product.id, Product.name, Product.category, Product.brand, Product.price,
                                 Product.image_url, Cart.quantity).join(Product, Cart.product_id == Product.id).all()
        line_items=[]
        if carts is not None:
         line_items = [{
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": item.name,
                },
                "unit_amount": int(item.price),  
            },
            "quantity": item.quantity,
        } for item in carts]
      

        try:
            checkout_session = stripe.checkout.Session.create(
                # success_url=domain_url +
                # "success?session_id={CHECKOUT_SESSION_ID}",
                payment_method_types=["card"],
                line_items=line_items,
                mode="payment",
                cancel_url=domain_url + "/cancel",
                success_url=domain_url + "success?session_id={CHECKOUT_SESSION_ID}"
            )
            
        except Exception as e:
            return jsonify(error=str(e)), 403

    return redirect(checkout_session.url, code=303)


@payment_bp.route("/success", methods=["GET"])
@login_required
def success():
    session_id = request.args.get('session_id')
    if session_id:
        session = stripe.checkout.Session.retrieve(session_id)
        payment = Payment(
                amount=session['amount_total'],
                currency=session['currency'],
                session_id=session['id'],
                status=session['payment_status'],
                created=session['created'],
                name=session['customer_details']['name'],
                email=session['customer_details']['email']
               )
        db.session.add(payment)
        db.session.commit() 
        cart_instance = Cart.query.all()
        for item in cart_instance:
           db.session.delete(item)
        db.session.commit()
        
    return render_template('success.html', session_id=session_id)


@payment_bp.route("/cancel", methods=["GET"])
@login_required
def cancel():
    if request.method == "GET":
        return render_template('cancel.html')
