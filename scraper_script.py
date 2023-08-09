from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
import time

chromedriver = './chromedriver' #Links to chrome driver in repo folder. 

# # Initialize Chrome WebDriver using executable_path parameter
# options = webdriver.ChromeOptions()
# options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'  # Path to Chrome application
driver = webdriver.Chrome()

driver.get("https://www.google.com")

input("Press enter to close the browser")
