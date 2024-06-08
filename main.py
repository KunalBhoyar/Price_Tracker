import time
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from amazon_config import (
    get_web_driver_options,
    get_firefox_web_driver,
    set_ignore_certificate_error,
    set_browser_as_incognito,
    NAME,
    CURRENCY,
    FILTERS,
    BASE_URL,
    DIRECTORY
)
from selenium.common.exceptions import NoSuchElementException
import json
from datetime import datetime

class GenerateReport:
    def __init__(self, file_name, filters, base_link, currency, data):
        self.data = data
        self.file_name = file_name
        self.filters = filters
        self.base_link = base_link
        self.currency = currency
        report = {
            'title': self.file_name,
            'date': self.get_now(),
            'best_item': self.get_best_item(),
            'currency': self.currency,
            'filters': self.filters,
            'base_link': self.base_link,
            'products': self.data
        }
        print("Creating report...")

        # Ensure the reports directory exists
        if not os.path.exists(DIRECTORY):
            os.makedirs(DIRECTORY)

        with open(f'{DIRECTORY}/{file_name}.json', 'w') as f:
            json.dump(report, f, indent=4)
        print("Done...")

    @staticmethod
    def get_now():
        now = datetime.now()
        return now.strftime("%d/%m/%Y %H:%M:%S")

    def get_best_item(self):
        try:
            return sorted(self.data, key=lambda k: k['price'])[0]
        except Exception as e:
            print(e)
            print("Problem with sorting items")
            return None

class AmazonAPI:
    def __init__(self, search_term, filters, base_url, currency):
        self.base_url = base_url
        self.search_term = search_term
        options = get_web_driver_options()
        set_ignore_certificate_error(options)
        set_browser_as_incognito(options)
        self.options = options
        self.currency = currency
        self.price_filter = f"&rh=p_36%3A{filters['min']}00-{filters['max']}00"

    def run(self):
        print("Starting Script...")
        print(f"Looking for {self.search_term} products...")
        links = self.get_products_links()
        if not links:
            print("Stopped script.")
            return
        print(f"Got {len(links)} links to products...")
        print("Getting info about products...")
        products = self.get_products_info(links)
        print(f"Got info about {len(products)} products...")
        return products

    def get_products_links(self):
        driver = get_firefox_web_driver(self.options)
        self.driver = driver
        self.driver.get(self.base_url)
        element = self.driver.find_element(By.XPATH, '//*[@id="twotabsearchtextbox"]')
        element.send_keys(self.search_term)
        element.send_keys(Keys.ENTER)
        time.sleep(5)  # wait to load page
        self.driver.get(f'{self.driver.current_url}{self.price_filter}')
        print(f"Our url: {self.driver.current_url}")
        time.sleep(5)  # wait to load page
        result_list = self.driver.find_elements(By.XPATH, '//div[@data-component-type="s-search-result"]')
        links = []
        try:
            for result in result_list:
                link_element = result.find_element(By.XPATH, ".//h2/a")
                links.append(link_element.get_attribute('href'))
            print(f"Found {len(links)} product links.")
            for link in links:
                print(link)
            self.driver.quit()
            return links
        except Exception as e:
            print("Didn't get any products...")
            print(e)
            self.driver.quit()
            return links

    def get_products_info(self, links):
        products = []
        for link in links:
            product = self.get_single_product_info(link)
            if product:
                products.append(product)
            print(f"Product details: {product}")
        return products

    def get_single_product_info(self, link):
        driver = get_firefox_web_driver(self.options)
        self.driver = driver
        print(f"Product URL: {link} - getting data...")
        self.driver.get(link)
        time.sleep(5)
        title = self.get_title()
        seller = self.get_seller()
        price = self.get_price()
        self.driver.quit()
        if title and seller and price:
            product_info = {
                'url': link,
                'title': title,
                'seller': seller,
                'price': price
            }
            return product_info
        return None

    def get_title(self):
        try:
            return self.driver.find_element(By.ID, 'productTitle').text
        except Exception as e:
            print(e)
            print(f"Can't get title of a product - {self.driver.current_url}")
            return None

    def get_seller(self):
        try:
            return self.driver.find_element(By.ID, 'bylineInfo').text
        except Exception as e:
            print(e)
            print(f"Can't get seller of a product - {self.driver.current_url}")
            return None

    def get_price(self):
        price = None
        try:
            price = self.driver.find_element(By.XPATH, "//span[@class='a-price']//span[@aria-hidden='true']").text
            price = self.convert_price(price)
        except NoSuchElementException:
            try:
                availability = self.driver.find_element(By.ID, 'availability').text
                if 'Available' in availability:
                    price = self.driver.find_element(By.CLASS_NAME, 'olp-padding-right').text
                    price = price[price.find(self.currency):]
                    price = self.convert_price(price)
            except Exception as e:
                print(e)
                print(f"Can't get price of a product - {self.driver.current_url}")
                return None
        except Exception as e:
            print(e)
            print(f"Can't get price of a product - {self.driver.current_url}")
            return None
        return price

    def convert_price(self, price):
        price = price.replace(self.currency, '').replace(',', '').strip()
        try:
            price = float(price)
        except ValueError:
            print(f"Error converting price: {price}")
            price = None
        return price

if __name__ == '__main__':
    am = AmazonAPI(NAME, FILTERS, BASE_URL, CURRENCY)
    data = am.run()
    if data:
        GenerateReport(NAME, FILTERS, BASE_URL, CURRENCY, data)
    else:
        print("No data to generate report.")
