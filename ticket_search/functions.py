import os
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from penny_pincher.settings import DEBUG


def get_condor():

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
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(chrome_options=chrome_options)
        # Run browser in regular mode
        # driver = webdriver.Chrome()

    URL = 'https://www.condor.com/us'
    driver.get(URL)

    # Accept necessary cookies
    try:
        accept_cookies_el = driver.find_element_by_css_selector(
            'div.cookie__body > ul > li:nth-child(2) > div > a')
        accept_cookies_el.click()

    except NoSuchElementException as err:
        print(err)

    # Click on city from
    time.sleep(5)
    city_from_el = driver.find_element_by_id('searchAirportOrigin')
    city_from_el.click()

    # Enter departure city
    time.sleep(1)
    departure_city_el = driver.find_element_by_id('airportinput_id_origin')
    departure_city_el.send_keys('Seattle', Keys.ENTER)

    title = driver.title

    driver.quit()

    # Print page title (we can use it to assert that we're on the correct page)
    return title
