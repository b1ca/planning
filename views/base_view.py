# coding=utf-8
from __future__ import unicode_literals
from helpers.waits import *
from pages.login_page import LoginPage
from views.archive_view import ArchiveView
from views.help_view import HelpView
from views.my_tasks_view import MyTasksView
from views.plans_list_view import PlansListView
from views.settings_view import SettingsView
from views.users_view import UsersView


class BaseView(object):

    def __init__(self, driver):
        self.driver = driver
        """
        @type driver: WebDriver
        """

    def navigate_my_tasks_view(self):
        self.driver.find_element_by_xpath("//span[.='Мои задачи']/ancestor::a").click()
        wait_until_extjs(self.driver, 10)
        return MyTasksView(self)

    def navigate_plans_list_view(self):
        self.driver.find_element_by_xpath("//span[.='Список планов']/ancestor::a").click()
        wait_until_extjs(self.driver, 10)
        return PlansListView(self)

    def navigate_users_view(self):
        self.driver.find_element_by_xpath("//span[.='Пользователи']/ancestor::a").click()
        wait_until_extjs(self.driver, 10)
        return UsersView(self)

    def navigate_archive_view(self):
        self.driver.find_element_by_xpath("//span[.='Архив']/ancestor::a").click()
        wait_until_extjs(self.driver, 10)
        return ArchiveView(self)

    def navigate_settings_view(self):
        self.driver.find_element_by_xpath("//span[.='Настройки']/ancestor::a").click()
        wait_until_extjs(self.driver, 10)
        return SettingsView(self)

    def navigate_help_view(self):
        self.driver.find_element_by_xpath("//span[.='Справка']/ancestor::a").click()
        wait_until_extjs(self.driver, 10)
        return HelpView(self)

    def logout(self):
        self.driver.find_element_by_xpath("//span[.='Выход']/ancestor::a").click()
        wait_until_extjs(self.driver, 10)
        return LoginPage(self)