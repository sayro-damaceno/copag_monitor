import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv


load_dotenv()

LOGIN_URL = "https://www.b2b.copagloja.com.br/login"
POKEMON_URL = "https://www.b2b.copagloja.com.br/pokemon"


payload = {"usuario": os.getenv("USUARIO"), "senha": os.getenv("SENHA")}
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"Erro ao enviar mensagem no Telegram: {e}")


driver = webdriver.Chrome()


def login():
    driver.get(LOGIN_URL)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'input[placeholder="Ex.: exemplo@mail.com"]')
        )
    )

    driver.find_element(
        By.CSS_SELECTOR, 'input[placeholder="Ex.: exemplo@mail.com"]'
    ).send_keys(payload["usuario"])

    driver.find_element(
        By.CSS_SELECTOR, 'input[placeholder="Adicione sua senha"]'
    ).send_keys(payload["senha"])

    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//button[@type="submit" and .//span[text()="Entrar"]]')
        )
    ).click()


def check_products():

    while True:
        driver.get(POKEMON_URL)
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//span[text()="Comprar"]'))
            )

            products = driver.find_elements(
                By.XPATH, '//article[.//span[text()="Comprar"]]'
            )

            # products_by_name = driver.find_elements(
            #     By.XPATH,
            #     '//article[.//span[text()="Comprar"] and contains(.//span[@class="vtex-product-summary-2-x-brandName"], "Charizard")]',
            # )

            if len(products) > 1:

                for product in products:
                    name = product.find_element(
                        By.CSS_SELECTOR, ".vtex-product-summary-2-x-brandName"
                    ).text

                    price = product.find_element(
                        By.CLASS_NAME, "vtex-product-price-1-x-currencyInteger--summary"
                    ).text

                    print(f"Product: {name} - Price: R$ {price}")
                    send_telegram_message(f"Product: {name} - Price: R$ {price}")

        except Exception as e:
            print(f"An error occurred: {e}")
            send_telegram_message(f"An error occurred: {e}")

        time.sleep(60)


try:
    login()
    time.sleep(5)
    send_telegram_message("Login successful. Starting product monitoring...")
    check_products()
finally:
    driver.quit()
