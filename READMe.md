# Customer Data Sync Application

## Overview

This application is designed to synchronize customer data between a local MySQL database and the Stripe payment platform, using Kafka for event-driven communication. It handles real-time updates from Stripe webhooks, polls for customer data, and ensures consistency across platforms.

## Why I Built This

I developed this application to deepen my understanding of several key technologies, including Kafka, Stripe webhooks, and real-time data synchronization. This project provided a hands-on approach to learning these concepts while building a functional and practical system.

## Application Details

### 1. Webhook Handling (`inward-sync.py`)
- A Flask server listens for Stripe webhooks (e.g., `customer.created`, `customer.updated`).
- It updates the local MySQL database with the received customer data, ensuring the local database is always in sync with Stripe.

### 2. Polling Service (`inward-sync-2.py`)
- This script continuously polls Stripe for any new or updated customers.
- It updates the local MySQL database, further ensuring data consistency.

### 3. Customer Update API and Kafka Producer (`outward.py`)
- Another Flask server provides an API endpoint to manually add or update customer data.
- Upon processing a request, it updates the MySQL database and produces a Kafka message to the `consumer-events` topic.

### 4. Kafka Consumer and Stripe Sync (`stripe-outward.py`)
- A Kafka consumer listens to the `consumer-events` topic for customer-related messages.
- Depending on the event (`add` or `update`), it interacts with Stripe to create or update customer records, ensuring data in Stripe reflects the latest changes.

### Folder Structure
- `inward-sync.py`: Webhook handling and database sync.
- `inward-sync-2.py`: Polling service for Stripe customer data.
- `outward.py`: API for customer updates and Kafka producer.
- `stripe-outward.py`: Consumes Kafka messages and updates Stripe.

## How to Run the Application

For detailed instructions on setting up and running the application, please refer to the `README.md` file located in the application's  directory. This file includes environment setup, dependencies, and step-by-step guidance to get the application running.

## Open for Improvement

This application is a learning project and is open to improvements. If you have any ideas for optimizing the process, implementing more efficient data synchronization, or enhancing the overall architecture, feel free to contribute or share your suggestions.

