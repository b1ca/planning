# coding=utf-8
from __future__ import unicode_literals
from base_page import BasePage


class MainPage(BasePage):

    def navigate_my_tasks_view(self):
        self.driver.find_element_by_xpath("//span[.='Мои задачи']/ancestor::a").click()
        from views.my_tasks_view import MyTasksView
        return MyTasksView(self.driver)

    def navigate_plans_list_view(self):
        self.driver.find_element_by_xpath("//span[.='Список планов']/ancestor::a").click()
        from views.plans_views import PlansListView

        return PlansListView(self.driver)

    def navigate_users_view(self):
        self.driver.find_element_by_xpath("//span[.='Пользователи']/ancestor::a").click()
        from views.users_view import UsersView

        return UsersView(self.driver)

    def navigate_archive_view(self):
        self.driver.find_element_by_xpath("//span[.='Архив']/ancestor::a").click()
        from views.archive_view import ArchiveView

        return ArchiveView(self.driver)

    def navigate_settings_view(self):
        self.driver.find_element_by_xpath("//span[.='Настройки']/ancestor::a").click()
        from views.settings_view import SettingsView

        return SettingsView(self.driver)

    def navigate_help_view(self):
        self.driver.find_element_by_xpath("//span[.='Справка']/ancestor::a").click()
        from views.help_view import HelpView

        return HelpView(self.driver)

    def navigate_arm_view(self):
        self.driver.find_element_by_xpath("//span[.='АРМ Руководителя']/ancestor::a").click()
        from views.arm_view import ARMView

        return ARMView(self.driver)