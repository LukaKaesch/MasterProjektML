import time
import os

from manufacturers import ManufacturerGanter, ManufacturerKipp
from helper import DIR_PATH, DOWNLOAD_DIR
from pages.login_page import LoginPage
from pages.start_page import StartPage
from pages.result_page import ResultPage
from pages.product_page import ProductPage
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from helper import create_folder


# Globals
EMAIL = 'ernst.diener@nordakademie.de'
PW = 'Ab123456'
SEARCH_TERM = 'Griff'
MANUFACTURER = ManufacturerKipp
MAX_RESULTS_PER_SEARCH_TERM = 30
ITERATION_MAX_FOR_SCROLLING = 3


# Configuration
DRIVER_PATH = 'geckodriver'
options = Options()
options.headless = False
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
options.set_preference("browser.download.folderList", 2)
options.set_preference("browser.download.manager.showWhenStarting", False)
options.set_preference("browser.download.dir", DOWNLOAD_DIR)
options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-gzip")
caps = webdriver.DesiredCapabilities().FIREFOX
caps["marionette"] = True
driver = webdriver.Firefox(options=options, capabilities=caps, executable_path=DRIVER_PATH)

# Main
login_page = LoginPage(driver)
login_page.login(EMAIL, PW)

start_page = StartPage(driver)
start_page.start_search(SEARCH_TERM)

result_page = ResultPage(driver)
result_page.select_mechanical_components()
result_page.select_manufacturers(MANUFACTURER.Name)
result_page.scroll_to_bottom(ITERATION_MAX_FOR_SCROLLING)
results = result_page.get_possible_results(MANUFACTURER)


for result in results:
    product_page = ProductPage(driver, MANUFACTURER, result.title)
    if not product_page.open_page(result.link): continue
    if not create_folder(product_page.product_dir, ''): continue
    product_page.save_image()
    if product_page.check_table_footer(): product_page.select_all_in_table()
    product_page.save_table()
    if not product_page.select_obj_as_download_format(): continue
    product_page.download_obj_files()


