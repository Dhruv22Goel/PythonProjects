import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import TimeoutException

# --- URLs ---
FORM_URL = 'https://docs.google.com/forms/d/e/1FAIpQLSezgJpMTyz_BhV1ud_NNltj5Z8xOWsKYiizdj50fs3oftaDxw/viewform?usp=header'
WEB_URL = 'https://appbrewery.github.io/Zillow-Clone/?'

# --- Scrape Zillow clone ---
web_content = requests.get(WEB_URL).text
soup = BeautifulSoup(web_content, 'html.parser')

# Prices
prices = soup.find_all("span", class_="PropertyCardWrapper__StyledPriceLine")
price_list = [price.text.split('+')[0].split('/')[0] for price in prices]

# Addresses + property links
address_s = soup.find_all("a", class_='StyledPropertyCardDataArea-anchor')
address_list = [address.text.strip() for address in address_s]
property_link_list = [address.get("href") for address in address_s]

# --- Form input XPaths ---
q1 = '''//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input'''
q2 = '''//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input'''
q3 = '''//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input'''

# --- Chrome setup ---
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)   # keeps browser open after script ends
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 20)

# --- Open the form ---
driver.get(FORM_URL)

# --- Fill & submit for each property ---
for q1_ans, q2_ans, q3_ans in zip(address_list, price_list, property_link_list):
    try:
        # Wait until inputs are clickable
        q1_input = wait.until(EC.element_to_be_clickable((By.XPATH, q1)))
        q2_input = wait.until(EC.element_to_be_clickable((By.XPATH, q2)))
        q3_input = wait.until(EC.element_to_be_clickable((By.XPATH, q3)))

        # Scroll into view
        driver.execute_script("arguments[0].scrollIntoView(true);", q1_input)

        # Fill answers
        q1_input.send_keys(q1_ans)
        q2_input.send_keys(q2_ans)
        q3_input.send_keys(q3_ans)

        # Submit
        submit_btn = driver.find_element(By.XPATH, '//span[text()="Submit"]/..')
        submit_btn.click()

        # Wait for confirmation
        time.sleep(2)

        try:
            # Look for "Submit another response" button
            another_btn = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//a[contains(text(),"Submit another response")]'))
            )
            another_btn.click()
        except TimeoutException:
            # fallback: reload form directly
            driver.get(FORM_URL)

    except TimeoutException:
        print("⚠️ Timeout – no form fields found, stopping.")
        break

print("✅ All form submissions completed.")
