import time
import sqlite3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('tweets.db')
cursor = conn.cursor()

# Create the table (if it doesn't exist)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tweets (
        id INTEGER PRIMARY KEY,
        handle TEXT,
        content TEXT,
        url TEXT
    )
''')
conn.commit()

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
    search_method.send_keys('crypto')
    search_method.send_keys(Keys.RETURN)


    latest = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Latest')))

    latest.click()

    # Set to keep track of collected tweets' content and handle
    collected_tweets = set()
    
    # Scroll down and collect tweets until there are no more new tweets
    while True:
        try: #waits for tweets to load
            tweets = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-testid="tweet"]')))
        except TimeoutException:
            print("Tweet error")
            tweets = []

        new_tweets = False
        
        for tweet in tweets:
            # Extract tweet text and twitter handle
            try:
                tweet_text = tweet.find_element(By.XPATH, './/div[@lang]').text
                twitter_handle = tweet.find_element(By.XPATH, './/span[contains(text(), "@")]').text
                        
                # Extract tweet_id from the href attribute of the a element containing the tweet text
                a = tweet.find_element(By.XPATH, './/a[contains(@href, "/status/")]')
                href = a.get_attribute('href')
                tweet_id = href.split('/')[-1]
        
                # Construct the tweet URL
                tweet_url = f'https://twitter.com/{twitter_handle}/status/{tweet_id}'


            except NoSuchElementException:
                continue
            
            # If the tweet is not already collected, process it
            tweet_data = (twitter_handle, tweet_text)
            if tweet_data not in collected_tweets:
                print("Handle:", twitter_handle)
                print("Content:", tweet_text)
                print("URL:", tweet_url)
                print("--------------------")
                # Add the tweet data to the collected tweets set
                collected_tweets.add(tweet_data)

                # Insert the tweet into the database
                cursor.execute('INSERT INTO tweets (handle, content, url) VALUES (?, ?, ?)', (twitter_handle, tweet_text, tweet_url))
                conn.commit()
                
                new_tweets = True
        
        # Scroll down
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        
        # Wait for some time to allow tweets to load
        time.sleep(5)

        
        # If there were no new tweets in the current batch, stop
        if not new_tweets:
            driver.refresh()

    # # Return the collected tweets
    # return list(collected_tweets)

# Call the function & if there is an error this ensures the databases closes correctly
try:
    tweets = tweet_data()
finally:
    cursor.close()
    conn.close()

input("Press enter to close the browser") #NOT IN USE CURRENTLY
# Close the WebDriver
driver.quit()
