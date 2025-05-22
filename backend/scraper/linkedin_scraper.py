# backend/scraper/linkedin_scraper.py

import json
import time
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Ajusta la ruta al chromedriver en tu máquina
CHROMEDRIVER_PATH = r"C:\WebDriver\chromedriver.exe"

# Ruta al JSON de cookies exportado desde tu sesión activa
COOKIES_PATH = os.path.join(os.path.dirname(__file__), "linkedin_cookies.json")


def load_cookies(driver, cookies_path):
    with open(cookies_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    for cookie in data.get("cookies", []):
        cookie_dict = {
            "name": cookie["name"],
            "value": cookie["value"],
            "domain": cookie["domain"],
            "path": cookie.get("path", "/"),
        }
        if "expirationDate" in cookie:
            cookie_dict["expiry"] = int(cookie["expirationDate"])
        driver.add_cookie(cookie_dict)


def init_driver():
    options = Options()
    # Modo headless y flags de entorno sin GPU ni sandbox
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # Deshabilitar diversas aceleraciones para evitar mensajes GPU/WebGL
    options.add_argument("--disable-gpu-compositing")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-accelerated-2d-canvas")
    options.add_argument("--disable-accelerated-video-decode")
    # Suprimir la mayoría de logs de Chromium
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("--log-level=3")
    # Deshabilitar WebRTC que provoca errores STUN
    options.add_argument("--disable-webrtc")
    options.add_argument("--disable-features=NetworkService,NetworkServiceInProcess")

    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    # Configurar timeouts
    driver.set_page_load_timeout(60)
    driver.set_script_timeout(60)
    driver.implicitly_wait(10)
    return driver


def main():
    driver = init_driver()

    # 1) Navegar a LinkedIn para establecer dominio y luego inyectar cookies
    driver.get("https://www.linkedin.com")
    time.sleep(2)

    load_cookies(driver, COOKIES_PATH)
    driver.refresh()
    time.sleep(2)

    print("Título tras login:", driver.title)

    # 2) Ejemplo: extraer seguidores
    driver.get("https://www.linkedin.com/feed/followers/")
    time.sleep(3)

    followers = driver.find_elements(By.CSS_SELECTOR, "li.reusable-search__result-container")
    print(f"Encontrados {len(followers)} seguidores")

    if followers:
        first = followers[0]
        name = first.find_element(By.CSS_SELECTOR, "span.entity-result__title-text a span[aria-hidden]").text
        photo = first.find_element(By.CSS_SELECTOR, "img.entity-result__image").get_attribute("src")
        print("Primer seguidor:", name, photo)

    # 3) Ejemplo: ir a tu perfil
    driver.get("https://www.linkedin.com/in/tu-perfil/")
    time.sleep(2)
    print("Página de perfil cargada:", driver.title)

    driver.quit()


if __name__ == "__main__":
    main()

