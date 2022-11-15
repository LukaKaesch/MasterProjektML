import time

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ResultPage:
    def __init__(self, driver):
        self.driver = driver

    def select_mechanical_components(self):
        mechanical_components_button = WebDriverWait(self.driver, 30)\
            .until(EC.presence_of_element_located((By.ID, 'TRACEPARTS:TP01')))
        self.driver.execute_script("arguments[0].click();", mechanical_components_button)

    def select_manufacturers(self, manufacturer_name):
        time.sleep(3)
        manufacturer_div = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//ul[@id="refine'
                                                                                                     '-list"]//li[2]/ul')))
        # Click on manufacturer in sidebar
        checkbox = manufacturer_div.find_element(By.XPATH,
                                                 '//label[contains(text(),"' + manufacturer_name + '")]/preceding::input[1]')
        self.driver.execute_script("arguments[0].click();", checkbox)

    def scroll_to_bottom(self, iteration_max):
        driver = self.driver
        scroll_pause_time = 1

        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

        for i in range(0, iteration_max):
            print('Log: Scrolling ', i, ' of ', iteration_max)

            try:
                button = driver.find_element(By.ID, 'searchresult-more')
                driver.execute_script("arguments[0].click();", button)

                # Scroll down to bottom
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # Wait to load page
                time.sleep(scroll_pause_time)

                # Calculate new scroll height and compare with last scroll height
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    try:
                        button = driver.find_element(By.ID, 'searchresult-more')
                        if not button.is_displayed(): break
                        driver.execute_script("arguments[0].scrollIntoView();", button)
                    except NoSuchElementException:
                        break
                    driver.execute_script("arguments[0].click();", button)
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                last_height = new_height
            except Exception as e:
                print('Log: Scrolling exception, ' + str(e))
                continue

    def get_possible_results(self, manufacturer_object):
        all_results = self.driver.find_element(By.ID, 'search-results-items').find_elements(By.XPATH, './*')
        filtered_results = manufacturer_object.filter_all_results(manufacturer_object, all_results)
        return filtered_results