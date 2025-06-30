from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

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

        try:
            enter_button = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "סטנדאפיסטים")))
            driver.execute_script("arguments[0].scrollIntoView(true);", enter_button)
            driver.execute_script("arguments[0].click();", enter_button)

            
        except TimeoutException:
            print("⚠️ button סטנדאפיסטים Not Found")
            return []

        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "elementor-heading-title")))

        headings = driver.find_elements(By.CLASS_NAME, "elementor-heading-title")
        for heading in headings:
            if artist.strip() in heading.text.strip():
                artist_link = heading.find_element(By.XPATH, "./ancestor::a[1]")
                artist_link.click()

                wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
                title = driver.find_element(By.TAG_NAME, "h1").text.strip()

                if artist.strip() in title:
                    print(f"✅ We got standup artist page{artist}")
                    print("🔗 URL:", driver.current_url)
                else:
                    print(f"❌ we got the page, but ({title}) is Compatible")

                break
        else:
            print("❌ Artist not on the List")

    except TimeoutException:
        print("⏳ Timeout - Not loaded on time")

    finally:
        driver.quit()


get_shows("שחר חסון")
