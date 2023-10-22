from confluent_kafka import Consumer, KafkaError
import json
import stripe

# Initialize the Stripe API with your API key
stripe.api_key = 'sk_test_51O41sQSAvARJ57IrqW1ilAFlNOZCne4bHFKHRmru9RgUbN7U3rUNAGuk4pIvqNfc3pzMjMO3VYGWFYnnDKpbDVmE00k9QtjKw5'

# Kafka consumer configuration.
kafka_consumer_config = {
    'bootstrap.servers': 'localhost:9092',  # Kafka broker address
    'group.id': 'customer-sync-group',
    'auto.offset.reset': 'earliest'
}
consumer = Consumer(kafka_consumer_config)
consumer.subscribe(['consumer-events'])

while True:
    msg = consumer.poll(1.0)

    if msg is None:
        continue

    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            print('Reached the end of the partition')
        else:
            print('Error while polling:', msg.error())
    else:
        # Process the customer event from Kafka.
        data = msg.value()
        
        # Ensure data is decoded as a string and then parse it as JSON
        try:
            data_str = data.decode('utf-8')
            data_dict = json.loads(data_str)

            # customer_id = data_dict.get('id')
            # name = data_dict.get('name')
            # email = data_dict.get('email')
            action = data_dict.get('action')

            print(data_dict)

            # Perform actions based on the data from Kafka
            if action == 'add':
                try:
                    # Create a new customer in Stripe
                    name = data_dict.get('name')
                    email = data_dict.get('email')
                    customer = stripe.Customer.create(
                        name=name,
                        email=email
                    )
                    print(f'Created customer {customer.id} in Stripe')
                except stripe.error.StripeError as e:
                    print('Error creating customer in Stripe:', str(e))
            elif action == 'update':
                try:
                    # Find the customer using previous email and name in Stripe
                    # Note: You would need to implement a mechanism to uniquely identify customers in Stripe.
                    # This may involve maintaining a mapping of your customer IDs to Stripe customer IDs.
                    # Here, we assume you can uniquely identify customers in Stripe based on their email and name.
                    prev_data = data_dict.get('prev')
                    updated_data = data_dict.get('updated')
                    customers = stripe.Customer.list(email=prev_data['email'])
                    
                    if len(customers.data) == 1:
                        # Assuming only one match is found in Stripe
                        customer = customers.data[0]
                        # print(customer)
                        # Update the customer's information in Stripe
                        stripe.Customer.modify(customer.id, name=updated_data['name'], email=updated_data['email'])
                        print(f'Updated customer {customer.id} in Stripe')
                    else:
                        print('No or multiple customers found for update in Stripe.')
                except stripe.error.StripeError as e:
                    print('Error updating customer in Stripe:', str(e))

        except json.JSONDecodeError as e:
            print('Error decoding JSON data:', str(e))
            continue

consumer.close()
