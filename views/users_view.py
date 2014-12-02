# coding=utf-8
from __future__ import unicode_literals
from helpers.waits import wait_until_url_contains, wait_until_extjs
from views.base_view import BaseView
from views.plans_views import ViewPlanView


class UsersView(BaseView):
    def __init__(self, driver):
        BaseView.__init__(self, driver)
        wait_until_url_contains(self.driver, 20, 'Users')
        wait_until_extjs(self.driver, 10)

    def choose_user(self, username):
        self.driver.find_element_by_xpath(
            "//div[contains(@id, 'gridview')]"
            "//ancestor::td[contains(@class, 'cell-first')]"
            "/div[contains(.,'%s')]" % username).click()
        wait_until_extjs(self.driver, 10)

    def navigate_view_plan_view(self):
        self.driver.find_element_by_xpath("//tr[@data-recordindex='0']//a").click()
        self.click_go_btn_warning()
        return ViewPlanView(self.driver)

    def click_go_btn_warning(self):
        self.driver.find_element_by_xpath(
            "//div[contains(@class, 'x-message-box')]//span[contains(.,'Продолжить')]/ancestor::a").click()
        wait_until_extjs(self.driver, 10)