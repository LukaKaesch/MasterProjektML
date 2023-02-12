import time
import traceback

from helper import *
from pages.login_page import LoginPage
from pages.start_page import StartPage
from pages.result_page import ResultPage
from pages.product_page import ProductPage
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from helper import create_folder

# Globals
EMAILS = ['sdfesfdsf@txen.de']
PW = 'Ab123456'
CREATE_NEW_SEARCH_RESULT_LIST = True
APPEND_NEW_SEARCH_RESULTS_TO_EXISTING_XML = True
AMOUNT_PER_CATEGORY = 3


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
    time.sleep(60)
    driver_new = init_config()
    login_page_new = LoginPage(driver_new)
    login_page_new.login(email, PW)
    print(f'Log: Changed account to {email}')
    return driver_new


directory = os.path.join(DIR_PATH, 'products\\')
dirs = [x[0] for x in os.walk(directory)]
for dir in dirs:
    if len(os.listdir(dir)) == 0:
        shutil.rmtree(dir)

# Main
change_account_check = False
email_iterator = 0
driver = init_config()
login_page = LoginPage(driver)
login_page.login(EMAILS[email_iterator], PW)

if CREATE_NEW_SEARCH_RESULT_LIST:
    start_page = StartPage(driver)
    start_page.start_search_by_mechanical_components()

    result_page = ResultPage(driver)
    result_page.search_by_components(AMOUNT_PER_CATEGORY, APPEND_NEW_SEARCH_RESULTS_TO_EXISTING_XML)

result_products_from_xml = get_products_from_xml_file()
iterator = 0
for result in result_products_from_xml:
    try:
        print(f'Log: Starting with result {iterator} of {len(result_products_from_xml)}')
        iterator += 1
        while not check_connection():
            print('Log: Trying to wait for an connection!')
        empty_tmp_downloads_directory()
        product_page = ProductPage(driver, result.title)
        if not product_page.open_page(result.link):
            continue
        product_page.set_manufacturer_name()
        if product_page.check_table_footer(): product_page.select_all_in_table()
        product_page.product_dir = create_classification_folder_structure(driver)
        if not create_folder(product_page.product_dir, product_page.product_title):
            remove_product_from_xml(result)
            print(f'Log: Removed product {product_page.product_title} from links.xml')
            continue
        product_page.product_dir = os.path.join(product_page.product_dir, product_page.product_title)
        product_page.save_table()
        if not product_page.select_obj_as_download_format():
            remove_product_from_xml(result)
            shutil.rmtree(product_page.product_dir)
            print(f'Log: Removed product {product_page.product_title} from links.xml')
            continue
        try:
            if product_page.pre_download_obj_files():
                remove_product_from_xml(result)
                print(f'Log: Removed product {product_page.product_title} from links.xml')
            else:
                shutil.rmtree(product_page.product_dir)
            if product_page.change_account:
                product_page.change_account = False
                email_iterator += 1
                driver = change_account(driver, email_iterator)
                continue
        except Exception as e:
            print('Log: Exception: ' + str(e))
            shutil.rmtree(product_page.product_dir)
            traceback.print_exc()
    except Exception as e:
        print('Log: Something went wrong!')
        traceback.print_exc()
