#coding=utf-8
from __future__ import unicode_literals
import logging
import sys
import unittest
import os
from datetime import datetime

from testconfig import config
from selenium import webdriver

from selenium.webdriver.remote.remote_connection import LOGGER
from pages.login_page import LoginPage


LOGIN = config['login']
PASS = config['pass']
LOGGER.setLevel(logging.WARNING)


class BaseTest(unittest.TestCase):

    driver = None
    current_view = None

    # @classmethod
    # def setUpClass(cls):
    #     cls.driver = webdriver.Firefox()
    #     cls.driver.maximize_window()

    def setUp(self):
        profile = webdriver.FirefoxProfile()
        profile.set_preference('browser.download.folderList', 2)
        profile.set_preference('browser.download.manager.showWhenStarting', False)
        profile.set_preference("browser.download.dir", os.getcwd())
        profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/xml')

        self.driver = webdriver.Firefox(profile)
        self.driver.maximize_window()
        self.driver.implicitly_wait(20)
        login_page = LoginPage(self.driver)
        login_page.navigate()
        self.current_view = login_page.login(LOGIN, PASS)

    def tearDown(self):
        if sys.exc_info()[0]:
            self.get_screenshot()
        if 'debug' not in config and self.driver:
            self.driver.quit()

    # @classmethod
    # def tearDownClass(cls):
    #     if 'debug' not in config and cls.driver:
    #         cls.driver.quit()

    def get_screenshot(self):
        """
        Save screenshot to test-results/method_name folder
        """
        method_name = self._testMethodName
        class_name = type(self).__name__
        time_now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        folder = os.path.dirname(os.getcwd())
        directory = "".join([folder, "/test-results/", class_name])

        if not os.path.exists(directory):
            os.makedirs(directory)

        file_name = "%s/%s - %s.png" % (directory, time_now, method_name)

        self.driver.get_screenshot_as_file(file_name)
        print "[[ATTACHMENT|%s]]" % file_name
        print "current url - %s" % self.driver.current_url

if __name__ == '__main__':
    unittest.main()