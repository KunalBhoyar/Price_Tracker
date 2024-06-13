import json
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def load_config():
    with open('config.json', 'r') as file:
        config = json.load(file)
    return config

def get_random_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    ]
    return random.choice(user_agents)

def get_proxies():
    return [
        "http://79.174.188.153:8080",
        "http://103.181.168.218:8080",
        "http://200.94.102.148:999"
    ]

def get_chrome_web_driver(options):
    return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

def set_ignore_certificate_error(options):
    options.add_argument('--ignore-certificate-errors')

def set_browser_as_incognito(options):
    options.add_argument('--incognito')

def set_headless(options):
    options.add_argument('--headless')

def set_proxy(options, proxy):
    options.add_argument(f'--proxy-server={proxy}')

def scrape_website(site_config, product_name):
    options = Options()
    options.add_argument(f"user-agent={get_random_user_agent()}")
    set_ignore_certificate_error(options)
    set_browser_as_incognito(options)
    set_headless(options)
    proxy = random.choice(get_proxies())
    set_proxy(options, proxy)

    driver = get_chrome_web_driver(options)
    search_url = f"{site_config['url']}{product_name.replace(' ', '+')}"
    driver.get(search_url)
    time.sleep(5)  # wait to load page
    print(f"Search URL: {search_url}")  # Debugging line
    print(f"Page Title: {driver.title}")  # Debugging line

    try:
        product_link_elements = driver.find_elements(By.CSS_SELECTOR, site_config["result_link_css"])
        if not product_link_elements:
            raise ValueError("Product link elements not found")

        product_links = [element.get_attribute('href') for element in product_link_elements]
        if not product_links:
            raise ValueError("Product links not found")

        driver.get(product_links[0])
        time.sleep(5)  # wait to load page

        price_element = driver.find_element(By.CSS_SELECTOR, site_config["price_css"])
        price = price_element.text.strip() if price_element else "Price not found"
    except Exception as e:
        print(f"Error: {e}")
        price = "Error occurred during scraping"
    finally:
        driver.quit()

    return price

def scrape_ebay(product_name):
    config = load_config()
    ebay_config = config["ebay"]
    return scrape_website(ebay_config, product_name)

def scrape_flipkart(product_name):
    config = load_config()
    flipkart_config = config["flipkart"]
    return scrape_website(flipkart_config, product_name)

def scrape_amazon_uk(product_name):
    config = load_config()
    amazon_uk_config = config["amazon_uk"]
    return scrape_website(amazon_uk_config, product_name)

if __name__ == '__main__':
    product_name = "iPhone 14"
    ebay_price = scrape_ebay(product_name)
    flipkart_price = scrape_flipkart(product_name)
    amazon_uk_price = scrape_amazon_uk(product_name)
    print(f"eBay Price: {ebay_price}")
    print(f"Flipkart Price: {flipkart_price}")
    print(f"Amazon UK Price: {amazon_uk_price}")
