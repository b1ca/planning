from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


def wait_until_extjs(driver, seconds_to_wait):
    jquery_is_ready = lambda x: driver.execute_script("return Ext.isReady == true")
    WebDriverWait(driver, seconds_to_wait).until(jquery_is_ready)


def wait_until_title_is_equal(driver, seconds_to_wait, title):
    WebDriverWait(driver, seconds_to_wait).until(ec.title_is(title))


def wait_until_text_present(driver, seconds_to_wait, locator, text):
    WebDriverWait(driver, seconds_to_wait).until(ec.text_to_be_present_in_element(locator, text))


def wait_until_main_page_loaded(driver, seconds_to_wait):
    pass