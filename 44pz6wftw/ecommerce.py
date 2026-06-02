from flask import Flask,jsonify,request
from pymongo import MongoClient
from bson.objectid import ObjectId

app=Flask(__name__)
client = MongoClient('mongodb+srv://vu241fa04b38_db_users:blessy@cluster0.rnxvpf4.mongodb.net/?appName=Cluster0')

db = client["ecommerce-db"]
users_collection = db["users"]
products_collection = db["products"]
cart_collection = db["cart"]
orders_collection = db["orders"]
print("Db Connected Successfully")

@app.route('/')
def home():
    return "Welcome to E-Commerce App"

@app.route('/users', methods=["GET"])
def get_users():
    users = list(users_collection.find())
    for user in users:
        user["_id"] = str(user["_id"])
    return jsonify(users)

@app.route('/users', methods=["POST"])
def add_user():
    data = request.get_json()
    user = {
        "name": data.get("name"),
        "email": data.get("email")
    }
    users_collection.insert_one(user)
    return jsonify({"message": "User added successfully"})

@app.route('/users/<id>', methods=["GET"])
def get_user(id):
    user = users_collection.find_one({"_id": ObjectId(id)})
    if user:
        user["_id"] = str(user["_id"])
        return jsonify(user)
    return jsonify({"message": "User not found"})

@app.route('/users/<id>', methods=["PUT"])
def update_user(id):
    data = request.get_json()
    updated_data = {
        "name": data.get("name"),
        "email": data.get("email")
    }
    users_collection.update_one({"_id": ObjectId(id)},
    {"$set": updated_data}
    )
    return jsonify({"message": "User updated successfully"})

@app.route('/users/<id>', methods=["DELETE"])
def delete_user(id):
    users_collection.delete_one({"_id": ObjectId(id)})
    return jsonify({"message": "User deleted successfully"})

@app.route('/products', methods=["GET"])
def get_products():
    products = list(products_collection.find())
    for product in products:
        product["_id"] = str(product["_id"])
    return jsonify(products)

@app.route('/products', methods=["POST"])
def add_product():
    data = request.get_json()
    product = {
        "name": data.get("name"),
        "price": data.get("price"),
        "quantity": data.get("quantity")
    }
    products_collection.insert_one(product)
    return jsonify({"message": "Product added successfully"})

@app.route('/products/<id>', methods=["PUT"])
def update_product(id):
    data = request.get_json()
    updated_data = {
        "name": data.get("name"),
        "price": data.get("price"),
        "quantity": data.get("quantity")
    }
    products_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": updated_data}
    )
    return jsonify({"message": "Product updated successfully"})

@app.route('/products/<id>', methods=["DELETE"])
def delete_product(id):
    products_collection.delete_one({"_id": ObjectId(id)})
    return jsonify({"message": "Product deleted successfully"})

@app.route('/cart', methods=["GET"])
def get_cart():
    cart_items = list(cart_collection.find())
    for item in cart_items:
        item["_id"] = str(item["_id"])
    return jsonify(cart_items)

@app.route('/cart', methods=["POST"])
def add_to_cart():
    data = request.get_json()
    cart_item = {
        "user_id": data.get("user_id"),
        "product_name": data.get("product_name"),
        "quantity": data.get("quantity"),
        "price": data.get("price")
    }
    cart_collection.insert_one(cart_item)
    return jsonify({"message": "Item added to cart"})

@app.route('/cart/<id>', methods=["DELETE"])
def delete_cart_item(id):
    cart_collection.delete_one({"_id": ObjectId(id)})
    return jsonify({"message": "Cart item deleted successfully"})

@app.route('/orders', methods=["GET"])
def get_orders():
    orders = list(orders_collection.find())
    for order in orders:
        order["_id"] = str(order["_id"])
    return jsonify(orders)

@app.route('/orders', methods=["POST"])
def place_order():
    data = request.get_json()
    order = {
        "user_id": data.get("user_id"),
        "products": data.get("products"),
        "total_amount": data.get("total_amount"),
        "status": "Placed"
    }
    orders_collection.insert_one(order)
    return jsonify({"message": "Order placed successfully"})

@app.route('/orders/<id>', methods=["PUT"])
def update_order(id):
    data = request.get_json()
    updated_data = {
        "status": data.get("status")
    }
    orders_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": updated_data}
    )
    return jsonify({"message": "Order updated successfully"})

@app.route('/orders/<id>', methods=["DELETE"])
def delete_order(id):
    orders_collection.delete_one({"_id": ObjectId(id)})
    return jsonify({"message": "Order deleted successfully"})

@app.errorhandler(404)
def unavailable_page(error):
    return jsonify({"message": "Sorry! This page is not available"})

if __name__ == "__main__":
    app.run(debug=True)


