from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class StartPage:
    def __init__(self, driver):
        self.driver = driver

    def start_search_by_mechanical_components(self):
        self.driver.get('https://www.traceparts.com/de/search/tracepartsklassifizierung-mechanische-komponenten'
                        '?CatalogPath=TRACEPARTS%3ATP01')
