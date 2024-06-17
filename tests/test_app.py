from flask import url_for
from Product.models import Product
from User.models import User
from User.views import check_password_hash
    
def test_registration(client, app):
    response = client.post("/register", data={
        "email": "visal204971@gmail.com",  
        "password": "12345",
        "name": "Vishal",
        "phone": "8826477727"
    })
    with app.app_context():
        assert User.query.count() == 3
        assert User.query.first().email == "visal204971@gmail.com"  
 


    
def test_login(client, app):
    response = client.post("/login", data={"email": "visal204971@gmail.com", "password": "12345"})
    with app.app_context():
      user = User.query.filter_by(email="visal204971@gmail.com").first()
      assert user is not None, "User should not exist"  
      assert check_password_hash(user.password,"12345"), "Password should match"
      assert response.status_code == 200
      
    token = response.headers.get('Set-Cookie')
    assert token is not None, "auth_token not found in cookies"
    

def test_post_create_product(client, app):
    new_product_data = {
        "name": "New Product",
        "brand": "BrandX",
        "category": "CategoryY",
        "price": "100",
        "description": "This is a new product.",
        "image_url": "http://example.com/image.jpg"
    }
    response = client.post("/create-product", data=new_product_data)
    # token = response.headers.get('Set-Cookie')
    # assert token is not None, "auth_token not found in cookies"
    with app.app_context():
        product = Product.query.filter_by(name="New Product").first()
        assert product is not None, "Product should be created"
        assert product.brand == "brandx"  
        assert product.category == "CategoryY"
        assert product.price == "100"
        assert product.description == "This is a new product."
        assert product.image_url == "http://example.com/image.jpg"