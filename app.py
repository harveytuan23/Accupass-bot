from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import sys


def make_webdriver() -> Chrome:
    options = create_options()
    driver = Chrome(ChromeDriverManager().install(),
                    options=options)

    return driver


def create_options() -> Options:
    options = Options()
    # options.add_argument("--headless")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")

    return options


def Click_Btn(by, value):
    try:
        button = WebDriverWait(_driver, 15).until(
            EC.visibility_of_element_located((by, value)))
        # button = _driver.find_element(by, value)
        time.sleep(0.5)
        button.click()
    except:
        print('error')

    return


def Click_Btn_refresh(by, value):
    success = False
    while (success == False):
        try:
            button = WebDriverWait(_driver, 2).until(
                EC.visibility_of_element_located((by, value)))
            # button = _driver.find_element(by, value)
            button.click()
            success = True
        except:
            _driver.refresh()
            success = False

    return


if __name__ == '__main__':
    # text = sys.argv[1]
    # result = text.upper()
    # print(result)

    with open('keyword.json') as f:
        keywords = json.load(f)

    url = "https://www.accupass.com/eflow/ticket/2303280702207269355030"
    _driver = make_webdriver()

    # Open browser
    _driver.get(url=url)

    # import cookies
    with open('session.json') as f:
        cookies = json.load(f)

    for cookie in cookies:
        _driver.add_cookie(cookie)
    _driver.refresh()
    time.sleep(5)

    # Scroll down the page
    _driver.execute_script("window.scrollBy(0, 500);")
    time.sleep(0.5)

    # Click +1 button
    Click_Btn_refresh(
        By.XPATH, "//div[@class='Ticket-df72ab0d-container']//*[contains(text(),'{}')]/following::span[@class='Ticket-7b1c6bff-add']".format(keywords['keyword']))

    # Click apply button
    Click_Btn(By.CLASS_NAME, "TicketSelect-f488fcfe-text-container")

    # Click agree checkbox
    Click_Btn(By.XPATH, "(//label//div)[1]")

    # Scroll down the page
    _driver.execute_script("window.scrollBy(0, 500);")
    time.sleep(0.5)

    # Click next button
    Click_Btn(By.XPATH,
              "//*[contains(text(),'下一步')]")
    time.sleep(5)

    _driver.quit()
