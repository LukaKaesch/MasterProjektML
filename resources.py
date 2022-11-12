import os
import urllib

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from Image import Image

DIR_PATH = os.path.dirname(os.path.realpath(__file__))


class ManufacturerGanter:
    Name = "GANTER"
    Image_Title = "Parameter Bild"

    def filter_all_results(self, all_results):
        filtered_results = []

        for r in all_results:
            print('Log: Filtering all results...')
            link = r.find_element(By.TAG_NAME, 'a').get_attribute('href')
            title = r.find_element(By.TAG_NAME, 'h5').text
            img = Image(title, link)
            if not img.is_already_saved(filtered_results):
                filtered_results.append(img)

        return filtered_results


class ManufacturerKipp:
    Name = "KIPP"
    Image_Title = "Zeichnung"

    def filter_all_results(self, all_results):
        filtered_results = []

        for r in all_results:
            print('Log: Filtering all results...')
            link = r.find_element(By.TAG_NAME, 'a').get_attribute('href')
            title = r.find_element(By.TAG_NAME, 'p').text
            img = Image(title, link)
            if not img.is_already_saved(filtered_results):
                filtered_results.append(img)

        return filtered_results

