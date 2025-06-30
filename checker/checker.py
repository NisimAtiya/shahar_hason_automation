from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import unquote



def get_shows(artist):
    options = Options()
    options.add_argument("--headless=new")  
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("https://comedybar.net/")
        wait = WebDriverWait(driver, 50)


        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "e-loop-item")))
        artist_blocks = driver.find_elements(By.CLASS_NAME, "e-loop-item")

        found = False
        for block in artist_blocks:
            h2 = block.find_element(By.TAG_NAME, "h2")

            if artist in h2.text:
                parent_link = block.find_element(By.XPATH, ".//ancestor::a[1]")
                driver.execute_script("arguments[0].scrollIntoView(true);", parent_link)
                driver.execute_script("arguments[0].click();", parent_link)


                wait.until(EC.presence_of_element_located((By.TAG_NAME, "h2")))
                title = driver.find_element(By.TAG_NAME, "h2").text.strip()


                if artist in title:
                    print(f"✅ We got {artist[::-1]} page")
                    print("🔗 URL:", unquote(driver.current_url))
                else:
                    print(f"❌ we got page {artist} but ({title}) Compatible")
                found = True
                break


    except TimeoutException:
        print("⏳ Timeout - Not loaded on time")

    finally:
        driver.quit()


get_shows("שחר חסון")