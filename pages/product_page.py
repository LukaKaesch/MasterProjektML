import shutil
import time
import os
import urllib.request
import csv
import zipfile

from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from helper import create_folder, move_file, create_product_information_xml \
    , check_if_download_finished, directory_exists, DIR_PATH, DOWNLOAD_DIR

DOWNLOAD_FAILED_COUNTER = 0


class ProductPage:
    def __init__(self, driver, manufacturer, product_title):
        self.change_account = False
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
        for title in self.manufacturer.Image_Title:
            try:
                image_link = self.driver.find_element(By.XPATH,
                                                      '//img[@title="' + title + '"]') \
                    .get_attribute('src')
                urllib.request.urlretrieve(image_link,
                                           'products/' + self.product_title + '/' + self.product_title + '.jpg')
                return
            except NoSuchElementException:
                continue

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
            self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + Keys.HOME)
            time.sleep(0.5)
            select.select_by_visible_text('OBJ')
            return True
        except Exception:
            print('Log: Obj is not available as download format')
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
        # Find partnumber and create directory
        download_div = self.get_available_downloads()
        if download_div is None: return
        part_number = download_div[0].find_element(By.XPATH, '//div[@class="download-partnumber"]').text
        if not create_folder(self.product_dir, part_number): return
        if not self.try_to_download_obj(part_number):
            shutil.rmtree(os.path.join(self.product_dir, part_number))
            return
        # Move file to correct directory und unzip
        file_name = os.listdir(DOWNLOAD_DIR)[0]
        if not move_file(DOWNLOAD_DIR + file_name, self.product_dir + part_number):
            shutil.rmtree(os.path.join(self.product_dir, part_number))
            return
        with zipfile.ZipFile(self.product_dir + part_number + '/' + file_name, "r") as zip_ref:
            zip_ref.extractall(self.product_dir + part_number)
        # Product Information XML is created
        create_product_information_xml(self.product_dir + part_number + '/',
                                       self.driver.current_url,
                                       self.manufacturer,
                                       part_number)
        os.remove(self.product_dir + part_number + '/' + file_name)

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
        table = self.driver.find_element(By.XPATH, '//div[@id="configuratorSteps"]//div[1]/table')
        table_rows = table.find_elements(By.CSS_SELECTOR, 'tr')
        # Repeat for all products on table on product page
        for i in range(1, len(table_rows)):
            # Click on table row to load new product
            row = self.driver.find_element(By.XPATH, '//tr[@data-row-id="' + str(i) + '"]')
            part_number = self.driver.find_element(By.XPATH, '//tr[@data-row-id="' + str(i) + '"]/td[2]').text
            if directory_exists(self.product_dir + part_number): continue
            self.driver.execute_script("arguments[0].click();", row)
            time.sleep(10)
            # Try to pre download the obj file and download it if successful
            download_button = self.driver.find_element(By.ID, 'direct-cad-download')
            self.driver.execute_script("arguments[0].click();", download_button)
            if self.check_if_download_successful(): self.download_obj()
            if self.change_account: break
            time.sleep(10)

