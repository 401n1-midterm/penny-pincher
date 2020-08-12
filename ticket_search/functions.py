import os
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from penny_pincher.settings import DEBUG


class SeleniumCondorSearch:

    def __init__(self):
        self.driver = None
        self.wait = None
        self.headless = True
        self.url = 'https://www.condor.com/us'

    def setup(self):
        if not DEBUG:
            # Settings for production
            chrome_options = webdriver.ChromeOptions()
            chrome_options.binary_location = os.environ.get(
                'GOOGLE_CHROME_BIN')
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--no-sandbox')
            driver = webdriver.Chrome(
                executable_path=os.environ.get('CHROMEDRIVER_PATH'),
                chrome_options=chrome_options)

        else:
            if self.headless:
                # Run driver in headless mode
                chrome_options = Options()
                chrome_options.add_argument('--headless')
                driver = webdriver.Chrome(chrome_options=chrome_options)
            else:
                # Run browser in regular mode
                driver = webdriver.Chrome()

        return driver

    def connect(self):
        self.driver.get(self.url)
        # wait until event happens, no longer than 15 sec
        wait = WebDriverWait(self.driver, 15)
        return wait

    def accept_cookies(self):
        try:
            accept_cookies_el = self.driver.find_element_by_css_selector(
                'div.cookie__body > ul > li:nth-child(2) > div > a')
            accept_cookies_el.click()
        except NoSuchElementException as err:
            print(err)

    def open_prices(self, departure_city, arrival_city):
        # Click on city from
        city_from_el = self.wait.until(
            EC.element_to_be_clickable((By.ID, 'searchAirportOrigin')))
        city_from_el.click()

        # Enter departure city
        departure_city_el = self.wait.until(
            EC.element_to_be_clickable((By.ID, 'airportinput_id_origin')))
        departure_city_el.send_keys(departure_city, Keys.ENTER)

        # Enter arrival city
        arrival_city_el = self.wait.until(
            EC.element_to_be_clickable((By.ID, 'airportinput_id_destination')))
        arrival_city_el.send_keys(arrival_city, Keys.ENTER)

    def get_prices(self):
        # Select all days
        time.sleep(1)  # wait for all page to load
        day_els = self.wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'uib-day')))

        day_els = self.driver.find_elements_by_class_name('uib-day')

        prices = []
        for el in day_els:
            try:
                price = el.find_element_by_class_name('price').text
                date = el.find_element_by_class_name('text-info').text
                prices.append({
                    'date':     date,
                    'price':    price
                })
            except NoSuchElementException as err:
                pass
        return prices

    def search(self, departure_city, arrival_city):
        self.driver = self.setup()
        self.wait = self.connect()
        self.accept_cookies()
        self.open_prices(departure_city, arrival_city)
        prices = self.get_prices()

        return prices

        self.driver.quit()


if __name__ == "__main__":
    search = SeleniumCondorSearch()
    prices = search.search('Seattle', 'Minsk')
    print(prices)
