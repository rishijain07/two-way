from confluent_kafka import Consumer, KafkaError

# Define the Kafka broker address
bootstrap_servers = 'localhost:9092'

# Create a Kafka consumer instance
consumer = Consumer({
    'bootstrap.servers': bootstrap_servers,
    'group.id': 'my-consumer-group',  # Replace with your consumer group name
    'auto.offset.reset': 'earliest'  # Set to 'latest' if you only want new messages
})

# Subscribe to the "customer-events" topic
consumer.subscribe(['customer-events'])

# Poll for messages
while True:
    msg = consumer.poll(1.0)  # Adjust the timeout as needed

    if msg is None:
        continue
    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            print('Reached end of partition')
        else:
            print('Error while consuming: {}'.format(msg.error()))
    else:
        # Process the message payload here
        print('Received message: {}'.format(msg.value()))

# Close the consumer when done
consumer.close()
