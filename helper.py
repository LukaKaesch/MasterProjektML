import glob
import os
import shutil
import time
import xml.etree.cElementTree as ET

from models import Product

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
DOWNLOAD_DIR = os.path.join(DIR_PATH, 'tmp_downloads\\')


def create_folder(dir_path, title):
    try:
        path_search_term = os.path.join(dir_path, title)
        os.mkdir(path_search_term)
        return True
    except Exception:
        print('Log: Folder "' + str(dir_path) + title + '" already exists.')
        return False


def move_file(source, destination):
    try:
        if os.path.isfile(source):
            shutil.move(source, destination)
            return True
    except Exception:
        return False


def get_products_from_xml_file():
    products = []
    tree = ET.parse(str(DIR_PATH + '/links.xml'))
    el_products = tree.find('Products').findall('Product')
    for el in el_products:
        p = Product(el.find('Title').text, el.find('Link').text)
        products.append(p)
    return products


def save_list_as_xml(list, append_new_results_check):
    existing_products = []
    if append_new_results_check:
        existing_products = get_products_from_xml_file()
    root = ET.Element("root")
    products = ET.SubElement(root, "Products")
    all_products = list + existing_products
    for l in all_products:
        product = ET.SubElement(products, "Product")
        ET.SubElement(product, "Link").text = l.link
        ET.SubElement(product, "Title").text = l.title
    tree = ET.ElementTree(root)
    ET.indent(tree, space="\t", level=0)
    tree.write("links.xml")


def create_product_information_xml(directory, url, manu, partn):
    try:
        root = ET.Element("root")
        product = ET.SubElement(root, "ProductInformation")
        ET.SubElement(product, "Url").text = url
        ET.SubElement(product, "Manufacturer").text = manu.Name
        ET.SubElement(product, "PartNumber").text = partn
        tree = ET.ElementTree(root)
        ET.indent(tree, space="\t", level=0)
        tree.write(directory + "ProductInformation.xml")
    except Exception:
        print('Log: Product information couldnt be created for: ' + url)


def remove_product_from_xml(product):
    tree = ET.parse(str(DIR_PATH + '/links.xml'))
    el_products = tree.find('Products').findall('Product')
    for prod in el_products:
        if prod.find('Link').text == product.link:
            tree.find('Products').remove(prod)
            tree.write("links.xml")
            break


def check_if_download_finished(path):
    time_to_wait = 2
    time_counter = 0
    while len(os.listdir(path)) == 0:
        time.sleep(0.5)
        time_counter += 1
        if time_counter > time_to_wait:
            return False
    return True


def empty_tmp_downloads_directory():
    shutil.rmtree(DOWNLOAD_DIR)
    os.makedirs('tmp_downloads')
