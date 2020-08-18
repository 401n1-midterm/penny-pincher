import calendar
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

from .models import SearchQuery, Result


class SeleniumCondorSearch:
    """Class for getting price on condor.com
    """

    def __init__(self):
        self.driver = None
        self.wait = None
        self.headless = True
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
        arrival_city_el.send_keys(arrival_city, Keys.ENTER)
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

        self.driver = self.setup()
        self.wait = self.connect()
        self.accept_cookies()
        self.open_prices(departure_city, arrival_city)
        departure_prices = self.get_prices()
        arrival_prices = self.get_prices(arrival=True)
        self.driver.quit()

        return (departure_prices, arrival_prices)


def run_search(search_id: str) -> tuple:
    search_query = SearchQuery.objects.get(pk=search_id)

    print('searh_query inside run_search', search_query)

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

    print(departure_prices)

    return {
        'departure_prices': departure_prices,
        'arrival_prices':   prices[1],
        'search_id':        search_id,
        'message':          message
    }


def get_cheapest_flights(data, search_query):
    departure_city = search_query.departure_city
    arrival_city = search_query.arrival_city
    date_from = search_query.date_from
    date_to = search_query.date_to
    duration =  search_query.stay_duration


    departures_prices = []
    arrival_prices = []
    cheapest_departures = []
    cheapest_arrivals = []

    cheapest_departure = 5000.00
    cheapest_arrival = 5000.00

    for ticket_info in data['departure_prices']:
        if ticket_info['date'] >= date_from and ticket_info['date'] <= date_to:
            if ticket_info['date'] == date_from:
                exact_date_from_price = Decimal(ticket_info['price'].split(' ')[1])
                print('exact_date_from_price', exact_date_from_price)
            departures_prices.append(ticket_info)

    for ticket_info in data['arrival_prices']:
        if ticket_info['date'] >= date_from and ticket_info['date'] <= date_to:
            if ticket_info['date'] == date_from:
                exact_date_return_price = Decimal(ticket_info['price'].split(' ')[1])
                print('exact_date_return_price', exact_date_return_price)
            arrival_prices.append(ticket_info)

    for price in departures_prices:
        if Decimal(price['price'].split(' ')[1]) <= cheapest_departure:
            cheapest_departure = Decimal(price['price'].split(' ')[1])
            cheapest_date = price['date']
            cheapest_departures.append(price)
    

    for price in arrival_prices:
        if Decimal(price['price'].split(' ')[1]) <= cheapest_arrival:
            cheapest_arrival = Decimal(price['price'].split(' ')[1])
            cheapest_date = price['date']
            cheapest_arrivals.append(price)

    results = []
    
    for departure in cheapest_departures:
        for arrival in cheapest_arrivals:
            if departure['date'] < arrival['date']:
                result = {
                    departure_city = search_query.departure_city
                    arrival_city = search_query.arrival_city
                    date_from = departure['date']
                    date_to = arrival['date']
                    price = departure['price'] + arrival['price']
                }

        result.append(result)
    
    return results