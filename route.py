from flask import Flask, request, jsonify
from datetime import datetime
import redis
import json

app = Flask(__name__)

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

@app.route('/api/orders', methods=['POST'])
def submit_order():
    try:
        user_id = int(request.form.get('userId', '').strip())
        product_id = int(request.form.get('productId', '').strip())
        quantity = int(request.form.get('quantity', '').strip())
    except (ValueError, AttributeError):
        return jsonify({"error": "userId, productId, and quantity must be integers"}), 400


    if user_id < 0 or product_id < 0 or quantity < 0:
        return jsonify({"error": "userId, productId, and quantity cannot be less than 0"}), 400

    order_id = r.incr("order_counter")

    order = {
        "id": order_id,
        "userId": user_id,
        "productId": product_id,
        "quantity": quantity,
        "createdAt": datetime.now().isoformat()
    }

    r.rpush("orders", json.dumps(order))

    return jsonify({"message": "Order submitted successfully", "data": order}), 201


@app.route('/api/orders', methods=['GET'])
def get_orders():
    orders_raw = r.lrange("orders", 0, -1)
    orders = [json.loads(order) for order in orders_raw]
    return jsonify({"orders": orders}), 200


if __name__ == '__main__':
    app.run(debug=True)
