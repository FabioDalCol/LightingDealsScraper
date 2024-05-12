from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Instantiate options
options = Options()

# Add extra options
options.add_argument("--window-size=1920,1080")  # Set the window size
options.add_argument("--disable-infobars")  # Disable the infobars
options.add_argument("--disable-popup-blocking")  # Disable pop-ups
options.add_argument("--ignore-certificate-errors")  # Ignore certificate errors
options.add_argument('--headless') # ensure GUI is off
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Set path to chromedriver as per your configuration
options.binary_location = '/bin/chromium'
webdriver_service = Service('/bin/chromedriver')

def chrome_driver():
    return webdriver.Chrome(service=webdriver_service, options=options)