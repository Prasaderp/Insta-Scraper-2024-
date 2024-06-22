import random
import time
import re
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from database import profile_col, hashtag_posts_col

def initialize_driver():
    options = Options()
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.94 Safari/537.36")
    options.add_argument("--disable-gpu") 
    options.add_argument("--headless") 
    driver = webdriver.Chrome(options=options)
    return driver

def quit_driver(driver):
    driver.quit()

def scrape_profile(username, is_private, driver):
    driver.get(f"https://www.instagram.com/{username}/")
    sleep(random.uniform(3, 5))

    ul_element = driver.find_element(By.CLASS_NAME, 'x78zum5')
    li_elements = ul_element.find_elements(By.TAG_NAME, 'li')

    posts_element = li_elements[0].find_element(By.CSS_SELECTOR, 'button span')
    followers_element = li_elements[1].find_element(By.CSS_SELECTOR, 'button span')
    following_element = li_elements[2].find_element(By.CSS_SELECTOR, 'button span')

    profile_data = {
        "username": username,
        "is_private": is_private,
        "No. of Posts": posts_element.text,
        "followers": followers_element.text,
        "following": following_element.text
    }

    profile_col.insert_one(profile_data)
    return profile_data

def scrape_post(driver, post_link):
    driver.get(post_link)
    time.sleep(2)

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    og_description = soup.find('meta', property='og:description')
    og_url = soup.find('meta', property='og:url')
    og_title = soup.find('meta', property='og:title')

    description_content = og_description['content'] if og_description else None
    post_url = og_url['content'] if og_url else None
    full_caption = og_title['content'] if og_title else None

    twitter_title = soup.find('meta', attrs={'name': 'twitter:title'})
    if twitter_title:
        account_name = twitter_title['content'].split('(')[-1].split(')')[0]
    else:
        account_name = None

    caption = re.sub(r'@\w+', '', full_caption) if full_caption else None
    hashtags = re.findall(r'#\w+', caption) if caption else None

    likes_match = re.search(r'(\d+,\d+|\d+) likes', description_content) if description_content else None
    date_match = re.search(r'(\b\w+\b \d{1,2}, \d{4})', description_content) if description_content else None

    likes_count = likes_match.group(1).replace(',', '') if likes_match else None
    likes_count = int(likes_count) if likes_count else None
    date = date_match.group(1) if date_match else None

    return {
        "post_url": post_url,
        "full_caption": caption,
        "hashtags": hashtags,
        "likes_count": likes_count,
        "date": date,
        "account_name": account_name 
    }

def scrape_hashtag_posts(hashtag, driver):
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(2)

    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")

    username_input.send_keys("neendbejar")
    password_input.send_keys("Son@li1234")
    password_input.send_keys(Keys.RETURN)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "svg[aria-label='Home']")))

    driver.get(f"https://www.instagram.com/explore/tags/{hashtag}/")
    time.sleep(5)

    posts = driver.find_elements(By.TAG_NAME, "a")
    post_links = [post.get_attribute("href") for post in posts if re.match(r'https://www.instagram.com/p/[A-Za-z0-9_-]+/', post.get_attribute("href"))]

    post_data = []

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(scrape_post, driver, post_link) for post_link in post_links]
        for future in futures:
            post_info = future.result()
            if post_info:
                post_data.append(post_info)

    hashtag_posts_col.insert_many(post_data)
    return post_data
