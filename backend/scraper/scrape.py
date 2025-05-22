# scraper/scrape.py
import os
import random
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()

LINKEDIN_USER = os.getenv("LINKEDIN_USER")
LINKEDIN_PASS = os.getenv("LINKEDIN_PASS")

def login(driver):
    driver.get("https://www.linkedin.com/login")
    time.sleep(random.uniform(2, 4))
    driver.find_element(By.ID, "username").send_keys(LINKEDIN_USER)
    driver.find_element(By.ID, "password").send_keys(LINKEDIN_PASS)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(random.uniform(3, 5))

def scrape_profile_data(driver, profile_url):
    driver.get(profile_url)
    time.sleep(random.uniform(2, 4))
    name = driver.find_element(By.CSS_SELECTOR, "h1").text
    followers = driver.find_element(By.CSS_SELECTOR, ".t-16.t-black.t-normal").text
    # Aquí añadirías lógica para últimas publicaciones y reacciones
    return {"url": profile_url, "name": name, "followers": followers}

def main():
    # Inicializa el navegador
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        login(driver)
        # Ejemplo: lista de URLs a scrapear
        urls = [
            "https://www.linkedin.com/in/usuario1/",
            # …
        ]
        data = []
        for url in urls:
            data.append(scrape_profile_data(driver, url))
            # Espera random entre scrapes
            time.sleep(random.uniform(60, 300))
        # Guarda como CSV
        import pandas as pd
        df = pd.DataFrame(data)
        df.to_csv("scraped_profiles.csv", index=False)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
