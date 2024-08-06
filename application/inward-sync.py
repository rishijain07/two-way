from flask import Flask, request, jsonify
import stripe
import mysql.connector
import pymysql

# Initialize the Flask application
app = Flask(__name__)

# Initialize the Stripe API with your secret API key
stripe.api_key = 'add_your_secret_key'

# MySQL Database Configuration
db = pymysql.connect(
    host="localhost",
    user="user_name",
    password="your_password",
    database="zenskar",
    cursorclass=pymysql.cursors.DictCursor  # To return results as dictionaries
)

@app.route('/stripe-webhook', methods=['POST'])
def stripe_webhook():
    try:
        data = request.get_json()
        event_type = data['type']

        if event_type == 'customer.created' or event_type == 'customer.updated':
            customer_id = data['data']['object']['description']
            name = data['data']['object']['name']
            email = data['data']['object']['email']

            # Sync the customer data to your local MySQL database
            cursor = db.cursor()
            if event_type == 'customer.created':
                cursor.execute("INSERT INTO customers (customer_id, name, email) VALUES (%s, %s, %s)", (customer_id, name, email))
            elif event_type == 'customer.updated':
                cursor.execute("UPDATE customers SET name = %s, email = %s WHERE customer_id = %s", (name, email, customer_id))
            db.commit()
            cursor.close()

        return jsonify({'status': 'Webhook received'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5002)
