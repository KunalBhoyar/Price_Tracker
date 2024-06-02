import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
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

def scrape_product(url):
    # Set up Selenium WebDriver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get(url)
    
    # Extract title and price using XPath
    try:
        title = driver.find_element(By.XPATH, '/html/body/div[4]/main/div[5]/div/div/div/div/div/div/div[4]/div[2]/div[2]/div[1]/div/div/div/div[2]/h1').text
    except:
        title = 'Title not found'
    
    try:
        price = driver.find_element(By.XPATH, '/html/body/div[4]/main/div[5]/div/div/div/div/div/div/div[4]/div[2]/div[2]/div[4]/div/div/div/div/div/div[1]/div[1]/div[1]/div[1]/div/span[1]').text
        # price_fraction = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/article/div[1]/div[2]/p[1]').text
        # price = price_whole + price_fraction
    except:
        price = 'Price not found'
    
    driver.quit()
    return {'title': title, 'price': price}

def store_product(product):
    collection.update_one({'title': product['title']}, {'$set': product}, upsert=True)

if __name__ == '__main__':
    product_urls = [
        'https://www.bestbuy.com/site/samsung-65-class-tu690t-crystal-uhd-4k-smart-tizen-tv/6538957.p?skuId=6538957',  # Replace with real product URLs
        'https://www.bestbuy.com/site/college-football-25-standard-edition-xbox-series-x-xbox-one/6584220.p?skuId=6584220',
        'https://www.bestbuy.com/site/stanley-5-gallon-wet-dry-vacuum-metal/6521428.p?skuId=6521428'
    ]
    
    for url in product_urls:
        product = scrape_product(url)
        store_product(product)
        print(f"Stored product: {product}")

        
