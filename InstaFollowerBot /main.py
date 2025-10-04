from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

USERNAME = ''
PASSWORD = ''
URL = 'https://www.instagram.com/'
TARGET_URL = 'https://www.instagram.com/chefsteps/'
brave_path = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"  # change this for your OS

options = webdriver.ChromeOptions()
options.binary_location = brave_path
options.add_experimental_option("detach", True)

user_data_dir = os.path.join(os.getcwd(), "brave_profile")
options.add_argument(f"--user-data-dir={user_data_dir}")

driver = webdriver.Chrome(options=options)
driver.get(URL)
wait = WebDriverWait(driver, 20)

# Wait for username and password fields
username = wait.until(EC.presence_of_element_located((By.NAME, "username")))
username.send_keys(USERNAME)

password = wait.until(EC.presence_of_element_located((By.NAME, "password")))
password.send_keys(PASSWORD)

# Wait for login button
submit_btn = wait.until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="loginForm"]/div[1]/div[3]/button'))
)
submit_btn.click()

driver.get(TARGET_URL)

followers = driver.find_element(By.CSS_SELECTOR, 'a[href="/chefsteps/followers/"]')
followers.click()
time.sleep(5)
driver.quit()