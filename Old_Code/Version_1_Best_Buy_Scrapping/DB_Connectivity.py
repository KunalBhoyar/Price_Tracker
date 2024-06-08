import os
from urllib.parse import quote_plus
from pymongo import MongoClient

# Retrieve environment variables
MONGO_USER = os.getenv('MONGO_USER')
MONGO_PASS = os.getenv('MONGO_PASS')
MONGO_HOST = os.getenv('MONGO_HOST', 'localhost')
MONGO_PORT = os.getenv('MONGO_PORT', '27017')
MONGO_DB = os.getenv('MONGO_DB', 'price_monitor')

# Print the retrieved environment variables for debugging
print(f"MONGO_USER: {MONGO_USER}")
print(f"MONGO_PASS: {MONGO_PASS}")
print(f"MONGO_HOST: {MONGO_HOST}")
print(f"MONGO_PORT: {MONGO_PORT}")
print(f"MONGO_DB: {MONGO_DB}")

# Ensure the environment variables are correctly retrieved
if not all([MONGO_USER, MONGO_PASS, MONGO_HOST, MONGO_PORT, MONGO_DB]):
    raise ValueError("One or more MongoDB environment variables are missing")

# Escape the MongoDB credentials
MONGO_USER_ESCAPED = quote_plus(MONGO_USER)
MONGO_ESCAPED = quote_plus(MONGO_PASS)

# Construct the MongoDB connection string
connection_string = f"mongodb://{MONGO_USER_ESCAPED}:{MONGO_USER_ESCAPED}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}"

# Print the connection string for debugging
print(f"Connection string: {connection_string}")

# Create the MongoClient object using the connection string
try:
    client = MongoClient(connection_string)
    client.admin.command('ping')
    print("Connected to MongoDB successfully")
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")
