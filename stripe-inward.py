from confluent_kafka import Consumer, KafkaError
import json  # Import the JSON module to parse the data

# Kafka consumer configuration.
kafka_consumer_config = {
    'bootstrap.servers': 'localhost:9092',  # Kafka broker address
    'group.id': 'customer-sync-group',
    'auto.offset.reset': 'earliest'
}
consumer = Consumer(kafka_consumer_config)
consumer.subscribe(['customer-events'])

while True:
    msg = consumer.poll(1.0)

    if msg is None:
        continue

    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            print('Reached end of partition')
        else:
            print('Error while polling:', msg.error())
    else:
        # Process the customer event from Kafka.
        data = msg.value()
        
        # Ensure data is decoded as a string and then parse it as JSON
        try:
            data_str = data.decode('utf-8')
            data_dict = json.loads(data_str)

            customer_id = data_dict.get('id')
            name = data_dict.get('name')
            email = data_dict.get('email')
            action = data_dict.get('action')
            print(data_dict)

            # Perform actions based on the data from Kafka
            # For example, update the customer in your Stripe account.
            # Note: You can uncomment and implement the Stripe logic.
            # if action == 'create_update':
            #     try:
            #         stripe.Customer.modify(customer_id, name=name, email=email)
            #         print(f'Updated customer {customer_id} in Stripe')
            #     except stripe.error.StripeError as e:
            #         print(f'Error updating customer {customer_id} in Stripe:', str(e))

        except json.JSONDecodeError as e:
            print('Error decoding JSON data:', str(e))
            continue

consumer.close()
