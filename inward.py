from flask import Flask, request, jsonify
import pymysql
from kafka import KafkaProducer
import json  # Import the json module

app = Flask(__name__)

# MySQL Database Configuration
db = pymysql.connect(
    host="localhost",
    user="root",
    database="zenskar",
    cursorclass=pymysql.cursors.DictCursor  # To return results as dictionaries
)
cursor = db.cursor()

# Kafka Producer Configuration
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)
print(producer.config)  # Print the Kafka producer configuration

@app.route('/update_customer', methods=['POST'])
def update_customer():
    data = request.get_json()
    print(data)
    try:
        data = request.get_json()
        id = data.get('id')
        name = data.get('name')
        email = data.get('email')
        action = data.get('action')  # 'add' or 'update'
        print(data)

        # Update local MySQL database
        if action == 'add':
            cursor.execute("INSERT INTO customers (id, name, email) VALUES (%s, %s, %s)", (id, name, email))
        elif action == 'update':
            cursor.execute("UPDATE customers SET name = %s, email = %s WHERE ID = %s", (name, email, id))
        else:
            return jsonify({"error": "str(e)"}), 500

        db.commit()

        # Produce Kafka message for the customer update
        kafka_message = {
            "id": id,
            "name": name,
            "email": email,
            "action": action
        }
        try:
            producer.send('customer-events', value=kafka_message)
        except Exception as kafka_error:
            print("Kafka send error:", kafka_error)

        return jsonify({"message": "Customer updated successfully."})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
