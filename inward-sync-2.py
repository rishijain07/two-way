import stripe
import time
import pymysql

# Initialize the Stripe API with your API key
stripe.api_key = 'add_your_sk_key'

# MySQL Database Configuration
db = pymysql.connect(
    host="localhost",
    user="your_username",
    password="your_password",
    database="zenskar",
    cursorclass=pymysql.cursors.DictCursor  # To return results as dictionaries
)
cursor = db.cursor()

# Define a timestamp to track the last sync
last_sync_timestamp = int(time.time())

# Polling interval in seconds
polling_interval = 10 

while True:
    try:
        # Query Stripe for customer updates since the last sync
        customers = stripe.Customer.list(
            created={'gte': last_sync_timestamp},
            limit=100  
        )

        for customer in customers.auto_paging_iter():
            customer_id = customer.description
            name = customer.name
            email = customer.email

            # Sync the customer data to your local database
            cursor.execute("SELECT * FROM customers WHERE ID = %s", (customer_id,))
            existing_customer = cursor.fetchone()

            if existing_customer:
                # Update the existing customer in your local database
                cursor.execute("UPDATE customers SET name = %s, email = %s WHERE ID = %s", (name, email, customer_id))
                print("updated customer")
            else:
                # Create a new customer in your local database
                cursor.execute("INSERT INTO customers (ID, name, email) VALUES (%s, %s, %s)", (customer_id, name, email))
                print("inserted customer")

            db.commit()

        # Update the last sync timestamp
        last_sync_timestamp = int(time.time())

        # Sleep for the polling interval before the next sync
        time.sleep(polling_interval)

    except stripe.error.StripeError as e:
        print('Error querying Stripe:', str(e))
    except Exception as e:
        print('Error:', str(e))
