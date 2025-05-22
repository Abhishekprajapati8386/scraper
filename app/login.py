import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time
import os
from dotenv import load_dotenv

load_dotenv()

IG_USERNAME = os.getenv("IG_USERNAME")
IG_PASSWORD = os.getenv("IG_PASSWORD")

def auto_login(driver):
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(3)

    try:
        username_input = driver.find_element(By.NAME, "username")
        password_input = driver.find_element(By.NAME, "password")
        username_input.send_keys(IG_USERNAME)
        password_input.send_keys(IG_PASSWORD)

        login_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
        login_button.click()

        time.sleep(5)

        if "challenge" in driver.current_url or "checkpoint" in driver.current_url:
            raise Exception("2FA or checkpoint challenge triggered.")
        print("Logged in successfully")
        return True
    except Exception as e:
        print(f"Login failed: {e}")
        return False
