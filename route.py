from flask import Flask, request, render_template
from datetime import datetime

app = Flask(__name__)
orders = []
order_counter = 1 

@app.route('/')
@app.route('/api/orders', methods=['POST'])
def submit_form():
    global order_counter  

    if request.method == 'POST':
        try:
            user_id = int(request.form['userId'])  
            product_id = int(request.form['productId'])
            quantity = int(request.form['quantity'])
        except (KeyError, ValueError):
            return {"error": "userId, productId, and quantity must be integers"}, 400

        if user_id < 0 or product_id < 0 or quantity < 0:
            return {"error": "userId, productId, and quantity cannot be less than 0"}, 400

        order = {
            "id": order_counter,
            "userId": user_id,
            "productId": product_id,
            "quantity": quantity,
            "createdAt": datetime.now().isoformat()
        }
        orders.append(order)
        order_counter += 1

        return {"message": "Form submitted successfully", "data": order}, 201
    else:
        return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)
