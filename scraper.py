import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
USERNAME=os.getenv('LINKEDIN_USERNAME')
PASSWORD=os.getenv('LINKEDIN_PASSWORD')
PROFILE_URL=os.getenv('LINKEDIN_PROFILE_URL')

# Using headless browser
# options = webdriver.ChromeOptions()
# options.add_argument('headless')
# driver = webdriver.Chrome(options=options)

# Or

options = Options()
options.add_argument("--no-sandbox")
options.add_argument('--headless=new')
options.add_argument("--disable-dev-shm-usage")
# options.add_argument('--window-size=1920,1200')
driver = webdriver.Chrome(options=options)

# driver = webdriver.Chrome()
driver.get('https://www.linkedin.com/login')
time.sleep(5)

username = driver.find_element(By.ID, 'username')
username.send_keys(USERNAME)

password = driver.find_element(By.ID, 'password')
password.send_keys(PASSWORD)

driver.find_element(By.XPATH, "//button[@type='submit']").click()

driver.get(PROFILE_URL)
time.sleep(3)

src = driver.page_source
soup = BeautifulSoup(src, 'html.parser')

profile = soup.find('div', {'class': 'artdeco-hoverable-content__content'})
is_verified = 'has verifications' in profile.text
print(is_verified)

driver.find_element(By.XPATH, "//*[@id='global-nav']/div/nav/ul/li[3]/a/span").click()
time.sleep(5)

src = driver.page_source
soup = BeautifulSoup(src, 'html.parser')

keyword = driver.find_element(By.XPATH, "//input[contains(@id, 'jobs-search-box-keyword-id')]")
keyword.send_keys('software engineer')
time.sleep(0.5)

location = driver.find_element(By.XPATH, "//input[contains(@id, 'jobs-search-box-location-id')]")
location.send_keys('Kigali')
time.sleep(2)

location.send_keys(Keys.RETURN)
time.sleep(5)

element_class = 'jobs-search-results-list'
scrollable_element = driver.find_element("css selector", "." + element_class)
# total_height = scrollable_element.size["height"]
total_height = driver.execute_script("return arguments[0].scrollHeight;", scrollable_element)

print(total_height)

scroll_increment = 100
current_position = 0

while current_position < total_height:
    driver.execute_script("arguments[0].scrollTop += arguments[1];", scrollable_element, scroll_increment)
    current_position += scroll_increment
    time.sleep(0.5)

html = driver.find_element(By.CLASS_NAME, "scaffold-layout__list-container")

# driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
titles = ['Job Title', 'Company', 'Location', 'Status', 'Application Link']
df = pd.DataFrame(columns = titles)

jobs = soup.find_all('li', {'class': 'jobs-search-results__list-item'})

for job in jobs:
    title = job.find('strong').text.strip()

    company = job.find('span', {'class': 'job-card-container__primary-description'}).text.strip()
    location = job.find('li', {'class': 'job-card-container__metadata-item'}).text.strip()
    status = job.find('div', {'class': 'job-card-container__job-insight-text'})
    status =  'N/A' if status is None else status.text.strip()
    link = job.find('a', href=True)['href']

    data = [job for job in (title, company, location, status, link)]

    length = len(df)
    df.loc[length] = data

df

from datetime import datetime
df.to_csv(r'./Data/jobs_{}.csv'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')), index=False)

# page = 0
# while page < 5:
#     src = driver.page_source
#     soup = BeautifulSoup(src, 'html.parser')
