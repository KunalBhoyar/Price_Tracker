import os
import requests
from pymongo import MongoClient
from urllib.parse import quote_plus

# Read MongoDB credentials from environment variables
MONGO_USER = os.getenv('MONGO_USER')
MONGO_PASS = os.getenv('MONGO_PASS')

# Escape MongoDB credentials
MONGO_USER_ESCAPED = quote_plus(MONGO_USER)
MONGO_PASS_ESCAPED = quote_plus(MONGO_PASS)

# Connect to MongoDB
client = MongoClient(f'mongodb://{MONGO_USER_ESCAPED}:{MONGO_PASS_ESCAPED}@localhost:27017/price_monitor')
db = client['price_monitor']
collection = db['products']

# Google API Key
API_KEY = 'AIzaSyB1PpAhYoEOhHlsoXS3teNa2LMOHuzfI7U'

def fetch_product_info(query):
    url = f'https://www.googleapis.com/shopping/search/v1/public/products?key={API_KEY}&country=US&q={query}'
    response = requests.get(url)
    data = response.json()
    return data.get('items', [])

def store_product(product):
    collection.update_one({'title': product['title']}, {'$set': product}, upsert=True)

if __name__ == '__main__':
    product_queries = [
        'Samsung 65 inch TV',
        'Xbox Series X',
        'Wet Dry Vacuum'
    ]
    
    for query in product_queries:
        products = fetch_product_info(query)
        for product in products:
            item = {
                'title': product['product']['title'],
                'price': product['product']['price']['amount'],
                'currency': product['product']['price']['currency'],
                'description': product['product'].get('description', ''),
                'link': product['product'].get('link', '')
            }
            store_product(item)
            print(f"Stored product: {item}")
