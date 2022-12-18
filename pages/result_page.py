import time

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helper import save_list_as_xml
from models import Product


class ResultPage:
    def __init__(self, driver):
        self.driver = driver

    def search_by_components(self, amount_per_classification, append_new_results_check):
        elements_classifications = self.driver.find_elements(By.XPATH, '//ul[@id="classif-list"]//a[@class="last"]')
        links_to_classifications = self.convert_elements_to_links(elements_classifications)
        products = []
        for link in links_to_classifications:
            self.driver.get(link)
            time.sleep(3)
            all_results = self.driver.find_element(By.ID, 'search-results-items').find_elements(By.XPATH, './*')
            results = self.get_specific_amount_of_results(amount_per_classification, all_results)
            products = products + self.convert_result_list_to_products(results)
        save_list_as_xml(products, append_new_results_check)

    def get_specific_amount_of_results(self, amount, all_results):
        try:
            results = all_results[0:amount]
            return results
        except Exception:
            return all_results[0:len(all_results) - 1]

    def convert_result_list_to_products(self, all_results):
        filtered_results = []

        for r in all_results:
            print('Log: Filtering all results...')
            link = r.find_element(By.TAG_NAME, 'a').get_attribute('href')
            title = r.find_element(By.TAG_NAME, 'h5').text
            img = Product(title, link)
            if not img.is_already_saved(filtered_results):
                filtered_results.append(img)

        return filtered_results

    def convert_elements_to_links(self, elements):
        links = []
        for el in elements:
            links.append(el.get_attribute('href'))
        return links

