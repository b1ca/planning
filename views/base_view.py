# coding=utf-8
from __future__ import unicode_literals
from helpers.waits import wait_until_extjs
from pages.main_page import MainPage


class BaseView(object):

    plan = None

    def __init__(self, driver):
        self.driver = driver
        """
        @type driver: WebDriver
        """
        wait_until_extjs(self.driver, 20)

    def navigate_plans_list_view(self):
        return MainPage(self.driver).navigate_plans_list_view()

    def navigate_my_tasks_view(self):
        return MainPage(self.driver).navigate_my_tasks_view()

    def navigate_users_view(self):
        return MainPage(self.driver).navigate_users_view()

    def navigate_archive_view(self):
        return MainPage(self.driver).navigate_archive_view()

    def navigate_settings_view(self):
        return MainPage(self.driver).navigate_settings_view()

    def navigate_help_view(self):
        return MainPage(self.driver).navigate_help_view()