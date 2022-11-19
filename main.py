import time
import traceback

from manufacturers import ManufacturerGanter, ManufacturerKipp
from helper import DOWNLOAD_DIR, get_products_from_xml_file, remove_product_from_xml, empty_tmp_downloads_directory
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
MANUFACTURER = ManufacturerGanter
MAX_RESULTS_PER_SEARCH_TERM = 1000
ITERATION_MAX_FOR_SCROLLING = 1000
CREATE_NEW_SEARCH_RESULT_LIST = False
APPEND_NEW_SEARCH_RESULTS_TO_EXISTING_XML = False


# Configuration
def init_config():
    DRIVER_PATH = 'geckodriver'
    options = Options()
    options.headless = False
    options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.download.alwaysOpenPanel", False)
    options.set_preference("browser.download.dir", DOWNLOAD_DIR)
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-gzip")
    caps = webdriver.DesiredCapabilities().FIREFOX
    caps["marionette"] = True
    return webdriver.Firefox(options=options, capabilities=caps, executable_path=DRIVER_PATH)


# Main
driver = init_config()
login_page = LoginPage(driver)
login_page.login(EMAIL, PW)

if CREATE_NEW_SEARCH_RESULT_LIST:
    start_page = StartPage(driver)
    start_page.start_search(SEARCH_TERM)

    result_page = ResultPage(driver)
    result_page.select_mechanical_components()
    result_page.select_manufacturers(MANUFACTURER.Name)
    result_page.scroll_to_bottom(ITERATION_MAX_FOR_SCROLLING)
    result_page.get_possible_results(MANUFACTURER, APPEND_NEW_SEARCH_RESULTS_TO_EXISTING_XML)

result_products_from_xml = get_products_from_xml_file()
iterator = 0
for result in result_products_from_xml:
    print(f'Log: Starting with result {iterator} of {len(result_products_from_xml)}')
    iterator += 1
    empty_tmp_downloads_directory()
    product_page = ProductPage(driver, MANUFACTURER, result.title)
    if not product_page.open_page(result.link):
        continue
    if not create_folder(product_page.product_dir, ''):
        remove_product_from_xml(result)
        continue
    product_page.save_image()
    if product_page.check_table_footer(): product_page.select_all_in_table()
    product_page.save_table()
    if not product_page.select_obj_as_download_format():
        continue
    try:
        product_page.pre_download_obj_files()
        remove_product_from_xml(result)
    except Exception as e:
        print('Log: Exception: ' + str(e))
        traceback.print_exc()

