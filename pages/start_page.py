from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class StartPage:
    def __init__(self, driver):
        self.driver = driver

    def start_search(self, search_term):
        driver = self.driver
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'searchBox'))).send_keys(search_term)
        driver.find_element(By.ID, 'search-button').click()