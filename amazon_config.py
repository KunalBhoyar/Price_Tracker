from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

DIRECTORY = 'reports'
NAME = 'laptop'
CURRENCY = 'USD'
BASE_URL = 'https://www.amazon.com/'
FILTERS = {
    'min': '500',
    'max': '1500'
}

def get_firefox_web_driver(options):
    return webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)

def get_web_driver_options():
    return webdriver.FirefoxOptions()

def set_ignore_certificate_error(options):
    options.set_preference("network.http.use-cache", False)

def set_browser_as_incognito(options):
    options.add_argument('--private')

def set_automation_as_head_less(options):
    options.headless = True
