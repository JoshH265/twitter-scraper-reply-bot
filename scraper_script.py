from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from bs4 import BeautifulSoup
import requests
import time

chromedriver = './chromedriver' #Links to chrome driver in repo folder. 

# # Initialize Chrome WebDriver using executable_path parameter
# options = webdriver.ChromeOptions()
# options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'  # Path to Chrome application
driver = webdriver.Chrome()


# # Wait for a few seconds for the login to complete
# time.sleep(5)
# # Navigate to the Twitter user's profile
# username = 'whyillbedamned'
# driver.get(f'https://twitter.com/{username}')


