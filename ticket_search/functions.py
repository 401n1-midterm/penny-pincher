import calendar
import os
import time
from datetime import datetime as dt
from decimal import Decimal

import lxml
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from penny_pincher.settings import DEBUG

from .models import Result, SearchQuery


class SeleniumCondorSearch:
    """Class for getting price on condor.com
    """

    def __init__(self):
        self.driver = None
        self.wait = None
        self.headless = False
        self.url = 'https://www.condor.com/us'

    def setup(self) -> object:
        """Setup driver
        """
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

    def connect(self) -> object:
        """Connect the driver to the given URL
        """
        self.driver.get(self.url)
        # wait until event happens, no longer than 15 sec
        wait = WebDriverWait(self.driver, 15)
        return wait

    def accept_cookies(self):
        """Click on 'Accept Cookies' button if it appears
        """
        try:
            time.sleep(1)
            accept_cookies_el = self.driver.find_element_by_css_selector(
                'div.cookie__body > ul > li:nth-child(2) > div > a')
            accept_cookies_el.click()
            time.sleep(2)
        except NoSuchElementException as err:
            print(err)

    def open_prices(self, departure_city: str, arrival_city: str) -> None:
        """Open Price calendar

        Args:
            departure_city (str): Departure city
            arrival_city (str): Arrival  city
        """
        # Click on city from
        city_from_el = self.wait.until(
            EC.element_to_be_clickable((By.ID, 'searchAirportOrigin')))
        city_from_el.click()
        time.sleep(1)

        # Enter departure city
        departure_city_el = self.wait.until(
            EC.element_to_be_clickable((By.ID, 'airportinput_id_origin')))
        departure_city_el.send_keys(departure_city, Keys.ENTER)
        time.sleep(1)

        # Enter arrival city
        arrival_city_el = self.wait.until(
            EC.element_to_be_clickable((By.ID, 'airportinput_id_destination')))
        arrival_city_el.send_keys(arrival_city)
        time.sleep(1)
        arrival_city_el.send_keys(Keys.ENTER)
        time.sleep(1)

    def convert_month(self, month_name: str) -> int:
        """Convert full month name into its number

        Args:
            month_name (str): Full month name (e.g. October)

        Returns:
            int: Month number (e.g. 10)
        """
        abbr_to_num = {name: num for num,
                       name in enumerate(calendar.month_abbr) if num}
        month_abbr = month_name[:3]

        return abbr_to_num[month_abbr]

    def get_prices(self, arrival=False) -> list:
        """Get prices from and corresponding dates

        Args:
            arrival (bool, optional): If True is passed in, will try to open the calendar. Defaults to False.

        Returns:
            list: List of objects in format {date: date, price: price}
        """
        prices = []

        if arrival:
            # Click on arrival city
            city_from_el = self.wait.until(
                EC.element_to_be_clickable((By.ID, 'searchAirportDestination')))
            city_from_el.click()
            time.sleep(1)

            # Open the calendar
            arrival_city_el = self.wait.until(
                EC.element_to_be_clickable((By.ID, 'airportinput_id_destination')))
            arrival_city_el.send_keys(Keys.ENTER)
            time.sleep(1)

        while True:
            # Wait for all page to load to avoid stale element error
            time.sleep(1.5)

            try:
                # If it's the last page
                overlay_message_el = self.driver.find_element_by_class_name(
                    'cst-search-flight-message__overlay')

                # Close calendar
                time.sleep(1)
                self.driver.find_elements_by_class_name(
                    'modal-link')[2].click()
                break
            except NoSuchElementException:
                pass

            # Wait until all elements are rendered
            day_els = self.wait.until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'uib-day')))

            # Get month and year
            month_name, year = self.driver.find_element_by_class_name(
                'ng-binding').text.split(' ')
            month_num = self.convert_month(month_name)

            # Select all day elements
            day_els = self.driver.find_elements_by_class_name('uib-day')

            # Genereate all available prices
            for el in day_els:
                try:
                    price = el.find_element_by_class_name('price').text
                    date = el.find_element_by_class_name('text-info').text

                    if price != '':
                        prices.append({
                            'date':     f'{year}-{month_num}-{date}',
                            'price':    price
                        })
                except NoSuchElementException as err:
                    pass

            self.driver.find_elements_by_class_name(
                'calendar__month__arrow')[1].click()

        return prices

    def search(self, departure_city: str, arrival_city: str) -> tuple:
        """Get all available departure and arrival flight prices for the given deparure and arrival cities

        Args:
            departure_city (str): Departure city
            arrival_city (str): Arrival city

        Returns:
            tuple: Tuple of lists with prices ([deparure], [arrival])
        """

        try:
            self.driver = self.setup()
            self.wait = self.connect()
            self.accept_cookies()
            self.open_prices(departure_city, arrival_city)
            departure_prices = self.get_prices()
            arrival_prices = self.get_prices(arrival=True)
        except:
            departure_prices = arrival_prices = []
        finally:
            self.driver.quit()

        return (departure_prices, arrival_prices)


def run_search(search_id: str) -> tuple:
    search_query = SearchQuery.objects.get(pk=search_id)

    departure_city = search_query.departure_city
    arrival_city = search_query.arrival_city

    search = SeleniumCondorSearch()
    message = ''

    try:
        prices = search.search(departure_city, arrival_city)
    except Exception as err:
        message = err
        prices = ({}, {})

    departure_prices = []
    for price in prices[0]:
        departure_prices.append(price)

    return {
        'departure_prices': departure_prices,
        'arrival_prices':   prices[1],
        'search_id':        search_id,
        'message':          message
    }


def get_cheapest_flights(data, search_query):

    def format_data(data):
        for i in range(len(data['departure_prices'])):
            formatted_date = dt.strptime(
                data['departure_prices'][i]['date'], "%Y-%m-%d")
            formatted_price = data['departure_prices'][i]['price'].split(' ')[
                1]
            data['departure_prices'][i]['date'] = formatted_date
            data['departure_prices'][i]['price'] = Decimal(formatted_price)

        for i in range(len(data['arrival_prices'])):
            formatted_date = dt.strptime(
                data['arrival_prices'][i]['date'], "%Y-%m-%d")
            formatted_price = data['arrival_prices'][i]['price'].split(' ')[1]
            data['arrival_prices'][i]['date'] = formatted_date
            data['arrival_prices'][i]['price'] = Decimal(formatted_price)

        return data

    def filter_by_date(data, search_query):
        departure_prices = []
        arrival_prices = []

        date_from = dt.strptime(str(search_query.date_from), "%Y-%m-%d")
        date_to = dt.strptime(str(search_query.date_to), "%Y-%m-%d")

        for date in data['departure_prices']:
            if date['date'] >= date_from and date['date'] <= date_to:
                departure_prices.append(date)

        for date in data['arrival_prices']:
            if date['date'] >= date_from and date['date'] <= date_to:
                arrival_prices.append(date)

        data['departure_prices'] = departure_prices
        data['arrival_prices'] = arrival_prices

        return data

    def filter_by_duration(data, search_query):
        results = []
        for departure_ticket in data['departure_prices']:
            for arrival_ticket in data['arrival_prices']:

                if arrival_ticket['date'] > departure_ticket['date']:
                    trip_duration = int(
                        str(arrival_ticket['date'] - departure_ticket['date']).split(' ')[0])

                    valid_duration = (trip_duration <= search_query.stay_duration + 3) and (
                        trip_duration >= search_query.stay_duration - 3) if search_query.stay_duration is not None else True

                    print(valid_duration)

                    if (valid_duration):
                        result = {
                            'departure_city': search_query.departure_city,
                            'arrival_city': search_query.arrival_city,
                            'date_from': departure_ticket['date'],
                            'date_to': arrival_ticket['date'],
                            'price': departure_ticket['price'] + arrival_ticket['price']
                        }

                        results.append(result)

        return results

    def get_cheapest_prices(results):
        output = []
        min_price = results[0]['price']

        for result in results:
            if result['price'] < min_price:
                min_price = result['price']

        for result in results:
            if result['price'] == min_price:
                output.append(result)

        return output

    # Execute helper functions
    format_data(data)
    filter_by_date(data, search_query)
    results = filter_by_duration(data, search_query)
    results = get_cheapest_prices(results)
    return results

def wait_page_facts():
  source = requests.get ('https://en.wikipedia.org/wiki/Wikipedia:On_this_day/Today').text
  soup = BeautifulSoup(source, 'lxml')
  facts = soup.find('div', class_="mw-parser-output").ul.li.text
#   print(facts)
#   facts = answer.find_all('li')
  return facts
#   return [{'name': f'Fact {i}', 'fact': fact.text} for i, fact in enumerate(facts)]
