import os
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from penny_pincher.settings import DEBUG


def get_condor(dep_city, arr_city):

    chrome_options = webdriver.ChromeOptions()

    if not DEBUG:
        chrome_options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(
            executable_path=os.environ.get('CHROMEDRIVER_PATH'),
            chrome_options=chrome_options)

    else:
        # chrome_options = Options()
        # chrome_options.add_argument('--headless')
        # driver = webdriver.Chrome(chrome_options=chrome_options)
        # Run browser in regular mode
        driver = webdriver.Chrome()

    URL = 'https://www.condor.com/us'
    driver.get(URL)
    # wait until event happens, no longer than 15 sec
    wait = WebDriverWait(driver, 15)

    # Accept necessary cookies
    try:
        accept_cookies_el = driver.find_element_by_css_selector(
            'div.cookie__body > ul > li:nth-child(2) > div > a')
        accept_cookies_el.click()

    except NoSuchElementException as err:
        print(err)

    # Click on city from
    city_from_el = wait.until(
        EC.element_to_be_clickable((By.ID, 'searchAirportOrigin')))
    city_from_el.click()

    # Enter departure city
    departure_city_el = wait.until(
        EC.element_to_be_clickable((By.ID, 'airportinput_id_origin')))
    departure_city_el.send_keys(dep_city, Keys.ENTER)

    # Enter arrival city
    arrival_city_el = wait.until(
        EC.element_to_be_clickable((By.ID, 'airportinput_id_destination')))
    arrival_city_el.send_keys(arr_city, Keys.ENTER)

    # Select all days
    time.sleep(1)  # wait for all page to load
    day_els = wait.until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'uib-day')))

    day_els = driver.find_elements_by_class_name('uib-day')

    prices = []
    for el in day_els:
        try:
            price = el.find_element_by_class_name('price').text
            date = el.find_element_by_class_name('text-info').text
            prices.append({
                'date':     date,
                'price':    price
            })
        except StaleElementReferenceException as err:
            print(err)
        except NoSuchElementException as err:
            pass
    print(prices)

    title = driver.title

    time.sleep(100)
    driver.quit()

    return title


if __name__ == "__main__":
    get_condor('Seattle', 'Minsk')
