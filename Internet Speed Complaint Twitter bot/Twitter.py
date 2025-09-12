from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import os
import pyperclip  # install with: pip install pyperclip

class Twitter:
    def __init__(self):
        URL = 'https://x.com/i/flow/login'
        brave_path = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"  # change this for your OS

        options = webdriver.ChromeOptions()
        options.binary_location = brave_path
        options.add_experimental_option("detach", True)

        # Reuse a profile (so you don’t have to log in every run)
        user_data_dir = os.path.join(os.getcwd(), "brave_profile")
        options.add_argument(f"--user-data-dir={user_data_dir}")

        self.driver = webdriver.Chrome(options=options)
        self.driver.get(URL)
        self.wait = WebDriverWait(self.driver, 20)

    def login(self, email, username, password):
        # Step 1: Enter email / phone
        email_input = self.wait.until(EC.presence_of_element_located((By.NAME, "text")))
        email_input.clear()
        email_input.send_keys(email)

        next_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Next"]/..')))
        next_btn.click()

        # Step 2: Username (only if Twitter asks)
        try:
            username_input = self.wait.until(EC.presence_of_element_located((By.NAME, "text")))
            username_input.clear()
            username_input.send_keys(username)

            name_next_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Next"]/..')))
            name_next_btn.click()
        except:
            pass  # skip if not asked

        # Step 3: Password
        password_input = self.wait.until(EC.presence_of_element_located((By.NAME, "password")))
        password_input.click()
        password_input.clear()

        # --- OPTION 1: slow typing (fixes special chars like @) ---
        for char in password:
            password_input.send_keys(char)
            sleep(0.1)


        sleep(1)  # let keystrokes register

        login_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Log in"]/..')))
        login_btn.click()


# -------------------------
# Usage
# -------------------------
TWITTER_EMAIL = ''
TWITTER_PASSWORD = ''
TWITTER_USERNAME = ''

test = Twitter()
test.login(TWITTER_EMAIL, TWITTER_USERNAME, TWITTER_PASSWORD)
