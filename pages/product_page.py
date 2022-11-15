import time
import os
import urllib.request
import csv
import shutil

from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from helper import create_folder, move_file, DIR_PATH, DOWNLOAD_DIR


class ProductPage:
    def __init__(self, driver, manufacturer, product_title):
        self.driver = driver
        self.manufacturer = manufacturer
        self.product_title = product_title
        self.product_dir = str(DIR_PATH + '/products/' + self.product_title + '/')

    def open_page(self, url):
        try:
            self.driver.get(url)
            # Timer to avoid IP Ban
            time.sleep(3)
            return True
        except Exception:
            return False

    def save_image(self):
        try:
            image_link = self.driver.find_element(By.XPATH,
                                                  '//img[@title="' + self.manufacturer.Image_Title + '"]') \
                .get_attribute('src')
        except NoSuchElementException:
            print('Log: No image found for "' + self.product_title + '" for title: ' + self.manufacturer.Image_Title)
            return

        urllib.request.urlretrieve(image_link, 'products/' + self.product_title + '/' + self.product_title + '.jpg')

    def check_table_footer(self):
        try:
            check = self.driver.find_element(By.ID, 'table-1-footer').is_displayed()
        except NoSuchElementException:
            return False
        return check

    def select_all_in_table(self):
        driver = self.driver
        try:
            select = driver.find_element(By.XPATH, '//div[@id="table-1-footer"]//div[1]/div[2]/div[1]/div[1]/button')
            driver.execute_script("arguments[0].click();", select)

            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//div[@id="table-1-footer"]//div[1]/div[2]/div[1]/div['
                                                            '1]/ul')))
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight/3);")
            time.sleep(0.5)

            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@id="table-1-footer"]//div[1]/div[2]/div[1]/div['
                                                      '1]/ul/li[4]'))).click()
        except (TimeoutException, NoSuchElementException):
            return

    def save_table(self):
        try:
            table = self.driver.find_element(By.XPATH, '//div[@id="configuratorSteps"]//div[1]/table')
            path = 'products/' + self.product_title + '/' + self.product_title + '.csv'
            with open(path, 'w', newline='') as csvfile:
                wr = csv.writer(csvfile)
                first_row = table.find_element(By.CSS_SELECTOR, 'tr')
                wr.writerow([d.text for d in first_row.find_elements(By.CSS_SELECTOR, 'th')])
                for row in table.find_elements(By.CSS_SELECTOR, 'tr'):
                    wr.writerow([d.text for d in row.find_elements(By.CSS_SELECTOR, 'td')])
        except NoSuchElementException:
            print('Log: No table found for - ' + self.product_title)

    def select_obj_as_download_format(self):
        try:
            select = Select(self.driver.find_element(By.ID, 'cad-format-select'))
            select.select_by_visible_text('OBJ')
            return True
        except Exception:
            print('Log: Obj is not available as download format')
            return False

    def pre_download_obj_files(self):
        table = self.driver.find_element(By.XPATH, '//div[@id="configuratorSteps"]//div[1]/table')
        table_rows = table.find_elements(By.CSS_SELECTOR, 'tr')

        for i in range(1, len(table_rows)):
            row = self.driver.find_element(By.XPATH, '//tr[@data-row-id="' + str(i) + '"]')
            self.driver.execute_script("arguments[0].click();", row)
            time.sleep(5)
            download_button = self.driver.find_element(By.ID, 'direct-cad-download')
            self.driver.execute_script("arguments[0].click();", download_button)
            time.sleep(5)
            break

    def download_obj_files(self):
        self.pre_download_obj_files()
        time.sleep(10)

        try:
            download_div = self.driver.find_element(By.XPATH, '//div[@id="dashboard-content-download-items"]//div[1]') \
                .find_elements(By.XPATH, './*')
        except NoSuchElementException:
            print('Log: No available downloads for: ' + self.product_title)
            return

        for dwl in download_div:
            part_number = dwl.find_element(By.XPATH, '//div[@class="download-partnumber"]').text
            if not create_folder(self.product_dir, part_number): continue

            self.driver.execute_script("arguments[0].click();", dwl)
            time.sleep(3)

            file_name = os.listdir(DOWNLOAD_DIR)[0]
            if not move_file(DOWNLOAD_DIR + file_name, self.product_dir + part_number): continue





