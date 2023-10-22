Sure, here's an updated set-up guide for your Stripe Customer Synchronization system, including instructions on how to run Inward Sync, expose it to Ngrok, and configure it for Stripe Webhooks. Please follow these steps:

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Python 3.x
- Flask
- Confluent Kafka (Python Client)
- Stripe API Key
- MySQL Server
- pymysql
- kafka-python
- Ngrok
- Apache Kafka 

### Step 1: Install Python Packages

```bash
pip install flask confluent-kafka stripe pymysql kafka-python
```

### Step 2: Start Kafka Locally

Start Kafka locally. You should have Kafka and Zookeeper running on your machine. You can use the following commands to start them:

```bash
# Start Zookeeper
bin/zookeeper-server-start.sh config/zookeeper.properties

# Start Kafka Server
bin/kafka-server-start.sh config/server.properties
```

### Step 3: Create Kafka Topic

Create a Kafka topic called "consumer-events" using the following command:

```bash
kafka-topics.sh --create --topic consumer-events --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

### Step 4: Database Setup

1. Create a MySQL database named `zenskar`.

2. Create a table named `customers` with the following structure:

   ```sql
   CREATE TABLE customers (
       id VARCHAR(255) PRIMARY KEY,
       name VARCHAR(255),
       email VARCHAR(255)
   );
   ```

### Step 5: Ngrok Setup

You need Ngrok to expose your local Flask server to the internet for Stripe Webhooks. Download Ngrok from [https://ngrok.com/download](https://ngrok.com/download) and unzip it.

Start Ngrok to create a public URL for your local server:

```bash
ngrok http http://127.0.0.1:5002
```

Ngrok will display a public URL that forwards to your local server (e.g., `https://your-ngrok-subdomain.ngrok.io`). Note this URL; you will use it for configuring the Stripe Webhook.

### Step 6: Configure Inward Sync (Flask with MySQL)

1. Open `inward-sync.py`.

2. Update the following configurations:
   - Stripe API key (line 13).
   - MySQL Database configurations (lines 21-26).

3. Start Inward Sync:

```bash
python inward-sync.py
```

### Step 7: Configure Stripe Webhook

1. Log in to your Stripe Dashboard.

2. Go to the "Developers" section and click on "Webhooks."

3. Click the "Add endpoint" button.

4. In the "Endpoint URL" field, enter the Ngrok URL you obtained earlier (e.g., `https://your-ngrok-subdomain.ngrok.io/stripe-webhook`).

5. Select the "customer.created" and "customer.updated" events.

6. Click the "Add endpoint" button to save the webhook.

### Step 8: Run Other Services

- Start the Stripe Outward Sync (Kafka Consumer):

```bash
python stripe-outward-sync.py
```

- Start the Outward Sync (Flask with Kafka Producer):

```bash
python outward.py
```

### Step 9: Running Inward Sync (Alternative)

Inward Sync (Flask with Stripe) provides an alternative script, inward-sync-2.py, that uses a polling mechanism to sync customer data. This script queries Stripe for customer updates at regular intervals.

   - Open inward-sync-2.py.
 
   - Update the Stripe API key (line 12).

   - Start Inward Sync (Alternative):

```bash

python inward-sync-2.py
```

Your Stripe Customer Synchronization system is now set up and running. The Inward Sync listens for Stripe Webhook events, and the Outward Sync allows you to add or update customers through the `/update_customer` endpoint.

Feel free to customize this setup further as needed for your project.