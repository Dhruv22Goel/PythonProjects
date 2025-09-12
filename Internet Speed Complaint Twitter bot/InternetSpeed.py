from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os


class InternetSpeed:
    def __init__(self):
        URL = 'https://www.speedtest.net/'
        brave_path = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"  # change this for your OS

        options = webdriver.ChromeOptions()
        options.binary_location = brave_path
        options.add_experimental_option("detach", True)

        user_data_dir = os.path.join(os.getcwd(), "brave_profile")
        options.add_argument(f"--user-data-dir={user_data_dir}")

        driver = webdriver.Chrome(options=options)
        driver.get(URL)

        # Wait for Start button and click
        start_btn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'start-button'))
        )
        start_btn.click()

        # Init values
        self.download_text = '—'
        self.upload_text = '—'

        # Wait until both values are updated
        while self.download_text == '—' or self.upload_text == '—':
            self.download_text = WebDriverWait(driver, 120).until(
                lambda d: (val := d.find_element(By.CSS_SELECTOR, "span[class$='download-speed']").text) != "" and val
            )

            self.upload_text = WebDriverWait(driver, 120).until(
                lambda d: (val := d.find_element(By.CSS_SELECTOR, "span[class$='upload-speed']").text) != "" and val
            )

        self.speedtest_result()  # so you actually see the result

    def speedtest_result(self):
        return (self.download_text, self.upload_text)
