import csv
from getpass import getpass
from time import sleep

from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Creates an instance of Chrome
driver = webdriver.Chrome()

# Open Twitter's login page
driver.get("https://twitter.com/login")

wait = WebDriverWait(driver, 10)  # Creates a maximum wait time of 10 seconds for each field

#Finds username field and inputs username then returns
username = wait.until(EC.presence_of_element_located((By.NAME, 'text')))
username.send_keys('JoshScraper265')
username.send_keys(Keys.RETURN) #Presses enter key

#Finds password field and inputs password then returns
password = wait.until(EC.presence_of_element_located((By.NAME, 'password')))
password.send_keys('JoshProject265!?')
password.send_keys(Keys.RETURN) #Presses enter key - logins into account

#Finds search box on twitter & inputs texts, then returns
search_method = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="SearchBox_Search_Input"]')))
search_method.send_keys('#BITCOIN')
search_method.send_keys(Keys.RETURN)

latest = driver.find_element(By.LINK_TEXT, 'Latest')

latest.click()

# Wait for tweets to load
tweets = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-testid="tweet"]')))

# Extract and print the contents and handles of the tweets
for tweet in tweets:
    tweet_text_element = tweet.find_element(By.XPATH, './/div[@lang]')
    handle_element = tweet.find_element(By.XPATH, './/span[contains(text(), "@")]')
   
    handle_element = handle_element.text
    tweet_text = tweet_text_element.text

    print("Handle:", handle_element)
    print("Content:", tweet_text)
    print("--------------------")


# Find all elements containing Twitter handles using XPath
# handles = driver.find_elements(By.XPATH, '//span[contains(@class, "username u-dir")]')


input("Press enter to close the browser")

# Close the WebDriver
driver.quit()