from confluent_kafka import Producer
import json

# Define the Kafka broker address
bootstrap_servers = 'localhost:9092'

# Create a Kafka producer instance
producer = Producer({'bootstrap.servers': bootstrap_servers})

# Define the topic to which you want to produce messages
topic = 'customer-events'

# Create a message payload in JSON format (customize as needed)
message_payload = {
    'customer_id': 1,
    'name': 'John Doe',
    'email': 'johndoe@example.com'
}

# Produce the message to the specified topic
producer.produce(topic, key='customer_id', value=json.dumps(message_payload))

# Wait for any outstanding messages to be delivered and delivery reports to be received
producer.flush()
