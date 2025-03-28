from flask import Flask, request, jsonify, render_template, session

app = Flask(__name__)
app.secret_key = "secret_key"  # For session handling

# Full menu with prices
menu_prices = {
    "coffee": 50, "tea": 30, "samosa": 20, "fries": 40, "idly": 35, "dosa": 50,
    "vada-sambar": 45, "sandwich": 60, "burger": 80, "pastry": 70, "pizza": 120,
    "pasta": 110, "smoothie": 90, "cold coffee": 75, "nuggets": 60
}

# Responses for the chatbot
responses = {
    "hello": "Hello! Welcome to our cafe. How can I assist you today?",
    "menu": ("We offer coffee, tea, snacks, idly, dosa, vada-sambar, "
             "samosas, fries, sandwiches, burgers, and pastries. What would you like?"),
    "snacks": "We have samosas, fries, and nuggets. What would you like?",
    "more": "We also have Pizza, Pasta, Cold Coffee, and Smoothies. What would you like?",
    "bill": "Your total is ₹{}. Would you like to proceed with payment?",
    "exit": "Thank you for visiting our cafe!",
    "unknown": "I'm sorry, I didn't understand that. Please ask about the menu, orders, or bill."

}

@app.route('/')
def home():
    session.clear()
    session['order'] = {}
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message", "").lower()

    if 'order' not in session:
        session['order'] = {}

    if user_message in responses:
        response = responses[user_message]
        if user_message == "bill":
            response = response.format(calculate_bill())
    elif user_message in menu_prices:
        session['order'][user_message] = session['order'].get(user_message, 0) + 1
        response = f"Your {user_message} has been added to the order for ₹{menu_prices[user_message]}. Current total: ₹{calculate_bill()} enter menu for more orders and bill for billing and exit to checkout"
    elif user_message in ["order", "my order"]:
        response = get_order_summary()
    elif user_message == "clear order":
        session['order'].clear()
        response = "Your order has been cleared. You can start a new ordr now."
    else:
        response = responses["unknown"]

    return jsonify({"response": response})

def calculate_bill():
    return sum(menu_prices[item] * quantity for item, quantity in session['order'].items())

def get_order_summary():
    if not session['order']:
        return "Your order is empty. Please add items first."
    summary = "\n".join(f"{item.capitalize()} x{quantity} - ₹{menu_prices[item] * quantity}"
                        for item, quantity in session['order'].items())
    return f"Here’s your order:\n{summary}\nTotal: ₹{calculate_bill()}."

if __name__ == '__main__':
    app.run(debug=True)
