from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
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
        button = WebDriverWait(_driver, 15, 2).until(
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

    with open('./dist/keyword.json') as f:
        keywords = json.load(f)

    url = "https://www.accupass.com/organizer/detail/1909260711508963461450"
    _driver = make_webdriver()
    set_time = keywords['time']

    # Open browser
    _driver.get(url=url)

    # import cookies
    with open('./dist/session.json') as f:
        cookies = json.load(f)

    for cookie in cookies:
        _driver.add_cookie(cookie)
    _driver.refresh()
    time.sleep(10)

    # Scroll down the page
    _driver.execute_script("window.scrollBy(0, 500);")
    time.sleep(3)

    # Click Friday event
    Click_Btn(By.XPATH, "//*[contains(text(),'週五')]")
    time.sleep(3)

    # Click register
    Click_Btn(By.CLASS_NAME, "OrgInfo-ef8556ff-register-button")
    time.sleep(3)

    # Refresh until 12:00pm
    while True:
        now_time = time.strftime("%H:%M:%S")
        print(now_time)
        if (now_time) == set_time:
            _driver.refresh()
            # Click "Choose ticket"
            Click_Btn(
                By.XPATH, "//select/option[@value='{}']".format(keywords['keyword']))
            break
        else:
            time.sleep(1)

    # Click +1 button
    Click_Btn(
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
