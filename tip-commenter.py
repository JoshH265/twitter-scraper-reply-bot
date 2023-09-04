import time
import sqlite3
import random

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains



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

def user_details():
    twitter_username = input("Please type twitter username >> ")
    twitter_password = input("Please type password >> ")
    return twitter_username, twitter_password


def tweet_data(twitter_username, twitter_password):

    text_selection = ["Reply Guy for $tip @tipcoineth", "Collecting $tip @tipcoineth", "I want to be top of $tip @tipcoineth", "Why do we want the $tip @tipcoineth",
                        "Give $tip @tipcoineth now", "More $tip @tipcoineth please", "Constantly stacking $tip @tipcoineth", "Not fading the $tip @tipcoineth", "Will cook the $tip @tipcoineth",
                        "$tip @tipcoineth", "$tip @tipcoineth increasing the engagement quite alot", "$tip @tipcoineth is a pretty interesting concept overall"]
    wait = WebDriverWait(driver, 10)  # Creates a maximum wait time of 10 seconds for each field

    #Finds username field and inputs username
    username = wait.until(EC.presence_of_element_located((By.NAME, 'text')))
    username.send_keys(twitter_username)

    username.send_keys(Keys.RETURN) #Presses enter key

    #Finds password field and inputs password
    password = wait.until(EC.presence_of_element_located((By.NAME, 'password')))
    password.send_keys(twitter_password)


    
    password.send_keys(Keys.RETURN) #Presses enter key - logins into account
            
    #Finds search box on twitter & inputs texts, then returns
    search_method = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="SearchBox_Search_Input"]')))
    # search_method.send_keys('-filter:replies $tip @tipcoineth')
    search_method.send_keys('$tip @tipcoineth')
    search_method.send_keys(Keys.RETURN)

    # USE THIS TO NAVIGATE TO THE LATEST TAB
    # latest = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Latest')))

    # latest.click()

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
                # Check if the tweet is an ad
                ad_element = tweet.find_elements(By.XPATH, './/span[text()="Ad"]')
                if ad_element:
                    continue

                a = tweet.find_element(By.XPATH, './/a[contains(@href, "/status/")]')
                href = a.get_attribute('href')
                tweet_text = tweet.find_element(By.XPATH, './/div[@lang]').text
                twitter_handle = tweet.find_element(By.XPATH, './/span[contains(text(), "@")]').text
                tweet_id = href.split('/')[-1]
                tweet_url = f'https://twitter.com/{twitter_handle}/status/{tweet_id}'

            except NoSuchElementException:
                continue
            except StaleElementReferenceException:
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

                #NEW CODE SECTION, AUTO COMMENTS ON TWEETS

                # Click on the tweet to open it in a new page
                tweet_url = f'https://twitter.com/{twitter_handle}/status/{tweet_id}'
                driver.execute_script(f'window.open("{tweet_url}", "_blank");')      

                driver.switch_to.window(driver.window_handles[1])
                
                # Wait for the comment box to be visible
                comment_box = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="tweetTextarea_0"]')))
                
                #Picks random text to send
                random_text = random.choice(text_selection)
                comment_box.send_keys(random_text)

                try:
                    problematic_div = driver.find_element(By.CSS_SELECTOR, 't')
                    driver.execute_script("arguments[0].remove();", problematic_div)
                except NoSuchElementException:
                    pass

                time.sleep(2)
                
                # reply_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="tweetButtonInline"]')))
                button = driver.find_element(By.CSS_SELECTOR, '[data-testid="tweetButtonInline"]')
                # driver.execute_script("arguments[0].scrollIntoView();", button)

                body = driver.find_element(By.TAG_NAME, 'body')
                for _ in range(5):
                    body.send_keys(Keys.ARROW_DOWN)
                    time.sleep(0.1)
                button.click()     
                time.sleep(3)

                # send_now_button = driver.find_element(By.CSS_SELECTOR, 'div[role="button"] > div > span > span')
                # send_now_button.click()
                # time.sleep(2)

                driver.close()
                # Switch back to the main window
                driver.switch_to.window(driver.window_handles[0])
                print("Navigated back")     



                # driver.execute_script("arguments[0].scrollIntoView();", reply_button)
                # driver.execute_script("arguments[0].click();", reply_button)

                # Navigate back to the search results page

                time.sleep(3)
                
                new_tweets = True
        
        # Scroll down
        # driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        print("About to scroll down")

        body = driver.find_element(By.TAG_NAME, 'body')
        for _ in range(50):
            body.send_keys(Keys.ARROW_DOWN)
            time.sleep(0.1)

        # Wait for some time to allow tweets to load
        time.sleep(3)

        
        # If there were no new tweets in the current batch, stop
        if not new_tweets:
            driver.refresh()

    # # Return the collected tweets
    # return list(collected_tweets)


#Runs function to collect login information
username, password = user_details()

# Creates an instance of Chrome
driver = webdriver.Chrome()

# Open Twitter's login page
driver.get("https://twitter.com/login")


# Call the function & if there is an error this ensures the databases closes correctly
try:
    tweet_data(username, password )
except Exception as e:
    print("An exception occurred:", e)
finally:
    cursor.close()
    conn.close()

input("Press enter to close the browser") #NOT IN USE CURRENTLY
# Close the WebDriver
driver.quit()
