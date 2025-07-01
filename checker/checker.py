from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import unquote
import time
import re





def get_shows(artist):

    # defining the driver 
    options = Options()
    options.add_argument("--headless=new")  
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # driver get to the main web page
        driver.get("https://comedybar.net/")
        wait = WebDriverWait(driver, 50)

        # In this section we looking for the specific artist from the main page - locate his page by using h2 and than got the right href
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

                # Making sure we go to the page of the right artist 
                if artist in title:
                    print(f"✅ We got {artist[::-1]} page")
                    print("🔗 URL:", unquote(driver.current_url))
                else:
                    print(f"❌ we got page {artist} but ({title}) Compatible")
                found = True
                break
        
        # We got to the artist page - now we mapping his shows to an array
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "elementor-icon-wrapper")))
        show_elements  = driver.find_elements(By.CLASS_NAME, "elementor-icon-wrapper")

        # Initialize the url array
        show_links = []

        # Initialize the shows that will be sended by email
        available_Shows = []


        # Locate the url's
        for show in show_elements:
            try:
                a_tag = show.find_element(By.TAG_NAME, "a")
                href = a_tag.get_attribute("href")
                if href:
                    show_links.append(unquote(href))
            except Exception as e:
                print("⚠️ url is not right!", e)


        # Remove duplicates from url's array
        show_links = list(set(show_links))
        print(f"🔎 found {len(show_links)} shows for {artist[::-1]}")

        # getting in each url, than recognize if there is availability of seats
        for show_url in show_links:
            driver.get(show_url)
            # fix the problem of page get reload after we search for the event details. resolve the DOM problem
            time.sleep(4)

            try:
            
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                all_divs = driver.find_elements(By.TAG_NAME, "div")

                # In case there is no tickets for the specific show
                for div in all_divs:
                    text = div.text.strip()
                    if text == "אזלו הכרטיסים באתר זה.":
                        break
            except Exception as e:
                print("⚠️ error with show page", e)
                

            try:
                # We letting the page get reload. than get the event details 
                driver.get(show_url)
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.text.show")))

                show_container = driver.find_element(By.CSS_SELECTOR, "div.text.show")

                
                theater_elem = show_container.find_element(By.CLASS_NAME, "theater")
                location = theater_elem.text.split("\n")[0].strip()
                location = re.sub(r"\(.*?\)", "", location).strip()


                date_elem = show_container.find_element(By.CLASS_NAME, "event-date")
                event_date = date_elem.text.strip()

                time_elem = show_container.find_element(By.CLASS_NAME, "event-time")
                event_time = time_elem.text.strip()

                print(f"🎭 location: {location[::-1]}")
                print(f"📅 date: {event_date[::-1]}")
                print(f"⏰ time: {event_time[::-1]}")

                available_Shows.append((location,event_date,event_time))
            
            except Exception as e:
                print("⚠️ error with show page", e)

    except TimeoutException:
        print("⏳ Timeout - Not loaded on time")

    
    

    finally:
        
        driver.quit()

        return available_Shows


