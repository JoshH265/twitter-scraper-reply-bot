import csv
from getpass import getpass
import time

from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException




# Creates an instance of Chrome
driver = webdriver.Chrome()

# Open Twitter's login page
driver.get("https://twitter.com/login")

def tweet_data():
    


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
    
    # Set to keep track of collected tweets' content and handle
    collected_tweets = set()
    
    # Scroll down and collect tweets until there are no more new tweets
    while True:
        tweets = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-testid="tweet"]')))
        
        new_tweets = False
        
        for tweet in tweets:
            # Extract tweet text and twitter handle
            try:
                tweet_text = tweet.find_element(By.XPATH, './/div[@lang]').text
                twitter_handle = tweet.find_element(By.XPATH, './/span[contains(text(), "@")]').text
            except StaleElementReferenceException:
                continue
            
            # If the tweet is not already collected, process it
            tweet_data = (twitter_handle, tweet_text)
            if tweet_data not in collected_tweets:
                print("Handle:", twitter_handle)
                print("Content:", tweet_text)
                print("--------------------")
                # Add the tweet data to the collected tweets set
                collected_tweets.add(tweet_data)
                
                new_tweets = True
        
        # Scroll down
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        
        # Wait for some time to allow tweets to load
        time.sleep(10)
        
        # If there were no new tweets in the current batch, stop
        if not new_tweets:
            break
    
    # Return the collected tweets
    return list(collected_tweets)

# Call the function
tweets = tweet_data()






input("Press enter to close the browser")

# Close the WebDriver
driver.quit()
