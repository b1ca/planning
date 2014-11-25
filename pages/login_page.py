# coding=utf-8
from __future__ import unicode_literals
from base_page import BasePage
from helpers.waits import wait_until_extjs
from views.my_tasks_view import MyTasksView
from helpers.extjs_elements import get_extjs_element


class LoginPage(BasePage):

    def login(self, login, password):
        wait_until_extjs(self.driver, 10)
        login_input = get_extjs_element(self, tag='input', extjs_locator='login_field')
        login_input.clear()
        login_input.send_keys(login)
        password_input = get_extjs_element(self, tag='input', extjs_locator='password_field')
        password_input.clear()
        password_input.send_keys(password)
        submit_btn = get_extjs_element(self, tag='a', extjs_locator='accent-button')
        submit_btn.click()
        return MyTasksView(self.driver)