import shutil
import time
import os
import csv
import zipfile

from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from helper import *

DOWNLOAD_FAILED_COUNTER = 0


class ProductPage:
    def __init__(self, driver, product_title):
        self.change_account = False
        self.driver = driver
        self.manufacturer = 'Keine Angabe'
        self.product_title = remove_forbidden_chars(product_title)
        self.product_dir = ''

    def set_manufacturer_name(self):
        try:
            manufacturer_element = self.driver.find_element(By.XPATH, '//div[@id="overview"]//img')
            self.manufacturer = manufacturer_element.get_attribute('title')
        except Exception:
            print(f'Manufacturer name not found for {self.product_title}')

    def open_page(self, url):
        try:
            self.driver.get(url)
            # Timer to avoid IP Ban
            time.sleep(3)
            return True
        except Exception:
            return False

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
            path = self.product_dir + '/different_variations.csv'
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
            select_el = self.driver.find_element(By.ID, 'cad-format-select')
            select = Select(select_el)
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center', inline: "
                                       "'center'});", select_el)
            time.sleep(0.5)
            select.select_by_visible_text('OBJ')
            self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + Keys.HOME)
            return True
        except Exception:
            print(f'Log: Obj is not available as download format for product {self.product_title}')
            return False

    def get_available_downloads(self):
        try:
            download_div = WebDriverWait(self.driver, 5) \
                .until(EC.presence_of_element_located((By.XPATH,
                                                       '//div[@id="dashboard-content-download-items"]//div[1]'))) \
                .find_elements(By.XPATH, './*')
            return download_div
        except NoSuchElementException:
            print('Log: No available downloads for: ' + self.product_title)
            return None

    def try_to_download_obj(self, part_number):
        attempts = 0
        while attempts < 4:
            try:
                obj = WebDriverWait(self.driver, 5) \
                    .until(EC.element_to_be_clickable((By.XPATH,
                                                       '//div[@id="dashboard-content-download-items"]//div['
                                                       '1]/a/div[2]/i')))
                obj.click()
                time.sleep(2)
                if not check_if_download_finished(DOWNLOAD_DIR):
                    attempts += 1
                    continue
                return True
            except Exception as e:
                attempts += 1
                time.sleep(3)
                print('Log: Trying again to download')
        print('Log: Download didnt work for: ' + part_number)
        return False

    def download_obj(self):
        try:
            # Find partnumber and create directory
            download_div = self.get_available_downloads()
            if download_div is None: return
            part_number = download_div[0].find_element(By.XPATH, '//div[@class="download-partnumber"]').text
            if not self.try_to_download_obj(part_number):
                shutil.rmtree(self.product_dir)
                return
            # Move file to correct directory und unzip
            file_name = os.listdir(DOWNLOAD_DIR)[0]
            if not move_file(DOWNLOAD_DIR + file_name, self.product_dir):
                shutil.rmtree(os.path.join(self.product_dir, part_number))
                return
            with zipfile.ZipFile(self.product_dir + '/' + file_name, "r") as zip_ref:
                zip_ref.extractall(self.product_dir)
            # Product Information XML is created
            create_product_information_xml(self.product_dir,
                                           self.driver.current_url,
                                           self.manufacturer,
                                           part_number)
            os.remove(self.product_dir + '/' + file_name)
            return True
        except Exception as e:
            print(f"Log: Excecption in download_obj: {e}")
            return False

    def check_if_download_successful(self):
        global DOWNLOAD_FAILED_COUNTER
        try:
            toast_container = WebDriverWait(self.driver, 10) \
                .until(EC.presence_of_element_located((By.CLASS_NAME, 'toast-message')))
            if toast_container.text == 'Ihre Anfrage wird bearbeitet. Die Datei wird für den Download erzeugt.' \
                    or toast_container.text == 'Apollo.DownloadCAD.Start.Message':
                print('Log: Download was successful!')
                DOWNLOAD_FAILED_COUNTER = 0
                return True
            print('Log: Download failed!')
            DOWNLOAD_FAILED_COUNTER += 1
            if DOWNLOAD_FAILED_COUNTER > 4:
                self.change_account = True
                DOWNLOAD_FAILED_COUNTER = 0
            return False
        except Exception:
            print('Log: Toast Container couldn\'t be found!')
            time.sleep(2)
            return False

    def pre_download_obj_files(self):
        time.sleep(10)
        # Try to pre download the obj file and download it if successful
        download_button = self.driver.find_element(By.ID, 'direct-cad-download')
        self.driver.execute_script("arguments[0].click();", download_button)
        if self.check_if_download_successful():
            if not self.download_obj(): return False
            time.sleep(10)
            return True
        else:
            return False
