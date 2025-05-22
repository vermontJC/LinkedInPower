# backend/scraper/linkedin_scraper_firestore.py

import json
import re
import random
import time
import os

import openai
from google.cloud import firestore
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ================= Configuración =================

# OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Firestore
# Asegúrate de tener GOOGLE_APPLICATION_CREDENTIALS apuntando a tu JSON de servicio
db = firestore.Client()

# Ruta driver chrome (puedes usar ChromeDriverManager o tu CHROMEDRIVER_PATH)
CHROMEDRIVER_PATH = r"C:\WebDriver\chromedriver.exe"

# Cookies exportadas
COOKIES_PATH = os.path.join(os.path.dirname(__file__), "linkedin_cookies.json")

# Número máximo de posts a extraer
MAX_POSTS = 20

# ================= Helpers =================

def load_cookies(driver, cookies_path):
    with open(cookies_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    for cookie in data.get("cookies", []):
        c = {
            "name": cookie["name"],
            "value": cookie["value"],
            "domain": cookie["domain"],
            "path": cookie.get("path", "/"),
        }
        if "expirationDate" in cookie:
            c["expiry"] = int(cookie["expirationDate"])
        driver.add_cookie(c)

def init_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu-compositing")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-accelerated-2d-canvas")
    options.add_argument("--disable-accelerated-video-decode")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("--log-level=3")
    options.add_argument("--disable-webrtc")
    options.add_argument("--disable-features=NetworkService,NetworkServiceInProcess")

    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(60)
    driver.implicitly_wait(10)
    return driver

# ================= Scraping & Firestore =================

def scrape_and_store_posts():
    driver = init_driver()

    # 1) Login via cookies
    driver.get("https://www.linkedin.com")
    time.sleep(2)
    load_cookies(driver, COOKIES_PATH)
    driver.refresh()
    time.sleep(3)
    print("✅ Autenticado, título:", driver.title)

    # 2) Ir al feed
    driver.get("https://www.linkedin.com/feed/")
    time.sleep(3)

    # 3) Scroll y recolectar posts
    posts = []
    attempts = 0
    while len(posts) < MAX_POSTS and attempts < 15:
        driver.execute_script("window.scrollBy(0, window.innerHeight);")
        time.sleep(random.uniform(1.5, 3.0))
        posts = driver.find_elements(By.CLASS_NAME, "feed-shared-update-v2")
        attempts += 1
        print(f"   Scroll {attempts}: encontrados {len(posts)} posts")
    posts = posts[:MAX_POSTS]

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "feed-shared-update-v2"))
    )

    # 4) Extraer, almacenar y mostrar
    for idx, post in enumerate(posts, 1):
        # Autor
        try:
            author = post.find_element(
                By.CSS_SELECTOR, ".feed-shared-actor__name, .update-components-actor__title"
            ).text.strip()
        except:
            author = "Desconocido"

        # Contenido
        try:
            content = post.find_element(
                By.CSS_SELECTOR, ".feed-shared-update-v2__description, .update-components-text"
            ).text.strip()
        except:
            content = ""

        # Reacciones
        try:
            react_btn = post.find_element(
                By.XPATH, ".//button[contains(@aria-label, 'reacción')]"
            )
            reactions = int("".join(filter(str.isdigit, react_btn.text))) if react_btn.text else 0
        except:
            reactions = 0

        # Comentarios
        try:
            comm_btn = post.find_element(
                By.XPATH, ".//button[contains(@aria-label, 'comentarios')]"
            )
            comments = int("".join(filter(str.isdigit, comm_btn.text))) if comm_btn.text else 0
        except:
            comments = 0

        # Menciones y hashtags
        mentions = re.findall(r'@(\w+)', content)
        hashtags = re.findall(r'#(\w+)', content)

        # Análisis GPT (tema | sentimiento)
        tema, sentimiento = "Indeterminado", "Indeterminado"
        try:
            resp = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Extrae 'TEMA | SENTIMIENTO' del texto."},
                    {"role": "user", "content": content}
                ]
            )
            out = resp.choices[0].message.content.strip()
            if "|" in out:
                tema, sentimiento = [x.strip() for x in out.split("|", 1)]
        except Exception as e:
            print(f"⚠️ GPT error en post {idx}: {e}")

        # Preparar datos
        doc_data = {
            "author": author,
            "content": content,
            "reactions": reactions,
            "comments": comments,
            "mentions": mentions,
            "hashtags": hashtags,
            "theme": tema,
            "sentiment": sentimiento,
            "scraped_at": firestore.SERVER_TIMESTAMP
        }

        # Almacenar en Firestore (colección 'posts')
        db.collection("posts").add(doc_data)
        print(f"🗄️ Guardado Post #{idx}: {author[:20]}...")

    driver.quit()
    print(f"\n🏁 Completado. Total posts almacenados: {len(posts)}")

if __name__ == "__main__":
    scrape_and_store_posts()
