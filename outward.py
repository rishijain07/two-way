from flask import Flask, request, jsonify
import pymysql
from kafka import KafkaProducer
import json  # Import the json module

app = Flask(__name__)

# MySQL Database Configuration
db = pymysql.connect(
    host="localhost",
    user="rishi",
    password="#Rishi123",
    database="zenskar",
    cursorclass=pymysql.cursors.DictCursor  # To return results as dictionaries
)
cursor = db.cursor()

# Kafka Producer Configuration
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)
# print(producer.config)  # Print the Kafka producer configuration

@app.route('/update_customer', methods=['POST'])
def update_customer():
    data = request.get_json()
    # print(data)
    try:
        data = request.get_json()
        id = data.get('id')
        name = data.get('name')
        email = data.get('email')
        action = data.get('action')  # 'add' or 'update'
        # print(data)

        # Update local MySQL database
        prev_name = ''
        prev_email = ''
        if action == 'add':
            cursor.execute("INSERT INTO customers (id, name, email) VALUES (%s, %s, %s)", (id, name, email))
        elif action == 'update':
            cursor.execute("SELECT * FROM customers WHERE id = %s", (id,))
            existing_customer = cursor.fetchone()

            if existing_customer:
                # If the customer exists, store the previous values
                prev_name = existing_customer['name']
                prev_email = existing_customer['email']

                # Update the customer's information in the database
                cursor.execute("UPDATE customers SET name = %s, email = %s WHERE id = %s", (name, email, id))
        else:
            return jsonify({"error": "str(e)"}), 500

        db.commit()

        # Produce Kafka message for the customer update
        kafka_message = {}
        if action == 'add':
            kafka_message = {
                "id": id,
                "name": name,
                "email": email,
                "action": action
            }
        elif action == 'update':
            kafka_message = {
                    "id": id,
                    "prev": {"name": prev_name, "email": prev_email},
                    "updated": {"name": name, "email": email},
                    "action": action
                }
        print(kafka_message)
        try:
            producer.send('consumer-events', value=kafka_message)
        except Exception as kafka_error:
            print("Kafka send error:", kafka_error)

        return jsonify({"message": "Customer updated successfully."})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
