import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
from app.login import auto_login
import json

def scrape_reels(username: str, limit: int = 20):
    print("Inside Function")
    options = uc.ChromeOptions()
    options.headless = False
    driver = uc.Chrome(options=options)

    try:
        if not auto_login(driver):
            raise Exception("Login failed")

        driver.get(f"https://www.instagram.com/{username}/reels/")
        time.sleep(3)
        print("Page Found")
        if "Sorry, this page isn't available." in driver.page_source:
            raise ValueError("User not found or account is private")

        scrolls = max(1, limit // 6)
        print(scrolls)
        for _ in range(scrolls):
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
            time.sleep(2)

        links = driver.find_elements(By.XPATH, '//a[contains(@href, "/reel/") or contains(@href, "/p/")]')
        reel_links = list({l.get_attribute('href') for l in links})[:limit]

        data = []

        for url in reel_links:
            print(url)
            driver.get(url)
            print("Url opened")
            time.sleep(3)
            try:
                video_url = driver.find_element(By.TAG_NAME, "video").get_attribute("src")
                # try:
                #     og_video = driver.find_element(By.XPATH, '//meta[@property="og:video"]')
                #     video_url = og_video.get_attribute("content")
                # except:
                #     video_url = None
                posted_at = driver.find_element(By.TAG_NAME, 'time').get_attribute("datetime")
                #caption_elem = driver.find_element(By.XPATH, "//div[contains(@class, '_a9zs')]")
                caption = ""
                try:
                    caption_elem = WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "xt0psk2")]/h1'))
                    )
                    caption = caption_elem.text
                    print("✅ Caption:", caption)
                except Exception as e:
                    print("⚠️ Caption not found:", e)
                    caption = ""


                # print(f'caption_elem {caption_elem}')
                # caption = caption_elem.text if caption_elem else ""
                # print(f"caption {caption}")
                # thumbnail = driver.find_element(By.TAG_NAME, "video").get_attribute("poster")
                # print(thumbnail)

                # Extracting likes count
                likes_count = None
                try:
                    likes_elem = driver.find_element(By.XPATH, '//span[@class="x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs xt0psk2 x1i0vuye xvs91rp x1s688f x5n08af x10wh9bi x1wdrske x8viiok x18hxmgj"]')
                    likes_count = likes_elem.text
                    print(f"✅ Likes: {likes_count}")
                except NoSuchElementException:
                    print("⚠️ Likes element not found.")

                data.append({
                    "id": url.split("/")[-2],
                    "reel_url": url,
                    "video_url": video_url,
                    # "thumbnail_url": thumbnail,
                    "caption": caption,
                    "posted_at": posted_at,
                    "views": None,
                    "likes": likes_count,
                    "comments": None
                })
            except NoSuchElementException:
                continue
        print(json.dumps({"source": "live", "data": data}, indent=4))
        return json.dumps({"source": "live", "data": data}, indent=4)
    finally:
        driver.quit()