# coding=utf-8
from __future__ import unicode_literals
from helpers.waits import wait_until_url_contains, wait_until_extjs
from views.base_view import BaseView


class UsersView(BaseView):
    def __init__(self, driver):
        BaseView.__init__(self, driver)
        wait_until_url_contains(self.driver, 20, 'Users')
        wait_until_extjs(self.driver, 10)

    def choose_user(self, username):
        pass