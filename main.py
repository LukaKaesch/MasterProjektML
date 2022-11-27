import time
import traceback

from manufacturers import ManufacturerGanter, ManufacturerKipp
from helper import DOWNLOAD_DIR, get_products_from_xml_file, remove_product_from_xml, \
    empty_tmp_downloads_directory, check_connection
from pages.login_page import LoginPage
from pages.start_page import StartPage
from pages.result_page import ResultPage
from pages.product_page import ProductPage
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from helper import create_folder

# Globals
EMAILS = ['te.sternst194@gmail.com',
          't.esternst194@gmail.com', 'ernst.diener@nordakademie.de', 'testernst194@gmail.com', 'test.ernst194@gmail.com', 'tes.ternst194@gmail.com']
PW = 'Ab123456'
SEARCH_TERM = 'Griff'
MANUFACTURER = ManufacturerGanter
MAX_RESULTS_PER_SEARCH_TERM = 1000
ITERATION_MAX_FOR_SCROLLING = 1000
CREATE_NEW_SEARCH_RESULT_LIST = False
APPEND_NEW_SEARCH_RESULTS_TO_EXISTING_XML = False


# Configuration
def init_config():
    driver_path = 'geckodriver'
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
    return webdriver.Firefox(options=options, capabilities=caps, executable_path=driver_path)


def change_account(driver_old, email_counter):
    try:
        email = EMAILS[email_counter]
    except Exception:
        print('Log: No accounts available anymore')
        quit()
    driver_old.close()
    time.sleep(300)
    driver_new = init_config()
    login_page_new = LoginPage(driver_new)
    login_page_new.login(email, PW)
    print(f'Log: Changed account to {email}')
    return driver_new


# Main
change_account_check = False
email_iterator = 0
driver = init_config()
login_page = LoginPage(driver)
login_page.login(EMAILS[email_iterator], PW)

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
    try:
        print(f'Log: Starting with result {iterator} of {len(result_products_from_xml)}')
        iterator += 1
        while not check_connection():
            print('Log: Trying to wait for an connection!')
        empty_tmp_downloads_directory()
        product_page = ProductPage(driver, MANUFACTURER, result.title)
        if not product_page.open_page(result.link):
            continue
        if product_page.check_table_footer(): product_page.select_all_in_table()
        if create_folder(product_page.product_dir, ''):
            product_page.save_image()
            product_page.save_table()
        if not product_page.select_obj_as_download_format():
            continue
        try:
            product_page.pre_download_obj_files()
            if product_page.change_account:
                product_page.change_account = False
                email_iterator += 1
                driver = change_account(driver, email_iterator)
                continue
            remove_product_from_xml(result)
        except Exception as e:
            print('Log: Exception: ' + str(e))
            traceback.print_exc()
    except Exception as e:
        print('Log: Something went wrong!')
        traceback.print_exc()
