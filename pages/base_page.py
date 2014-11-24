# coding=utf-8
from __future__ import unicode_literals


class BasePage(object):
    url = 'http://185.4.229.80:8520/'

    def __init__(self, driver):
        self.driver = driver
        """
        @type driver: WebDriver
        """

    def navigate(self):
        self.driver.get(self.url)