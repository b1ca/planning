# coding=utf-8
from __future__ import unicode_literals
from selenium.webdriver import ActionChains
from views.base_view import BaseView
from helpers.waits import wait_until_extjs, wait_until_url_contains
import time
import random


class PlansListView(BaseView):
    def get_new_plan_form(self):
        self.driver.find_element_by_xpath("//span[.='Новый план']/ancestor::a").click()
        wait_until_extjs(self.driver, 10)
        return self.driver.find_element_by_xpath(
            "//span[.='Создать новый план']/ancestor::div[contains(@class, 'x-window-closable')]")

    def create_new_plan(self):
        plan_form = self.get_new_plan_form()
        plan = Plan(self.driver)
        plan.get_calendar_and_task(plan_form)
        plan.fill_form()
        self.plan = plan
        return EditPlanView(self.driver)


class Plan(object):
    def __init__(self, driver):
        self.driver = driver
        """
        @type driver: WebDriver
        """
        self.title = 'plan_title_%s' % str(int(round(time.time() * 1000)))
        self.description = 'cool description'
        self.calendar = None
        self.task = None
        self.date = str(time.localtime(time.time())[2])
        self.time = '23:45'

    def fill_form(self):
        self.driver.find_element_by_css_selector('input[name=Title]').send_keys(self.title)
        self.driver.find_element_by_css_selector('textarea[name=Description]').send_keys(self.description)
        self.driver.find_element_by_xpath("//table[contains(@id,'datefield')]//div[@role='button']").click()
        self.driver.find_element_by_xpath("//td[@title='Сегодня']/a").click()
        self.driver.find_element_by_xpath("//table[contains(@id,'timefield')]//div[@role='button']").click()
        self.driver.find_element_by_xpath("//li[contains(@class,'x-boundlist-item')][.='%s']" % self.time).click()
        self.driver.find_element_by_xpath("//span[.='Создать']/ancestor::a").click()
        wait_until_extjs(self.driver, 10)

    def get_calendar_and_task(self, plan_form):
        plan_form.find_element_by_xpath("//input[@name='CalendarId']/ancestor::tr//div[@role='button']").click()
        wait_until_extjs(self.driver, 10)
        calendar_list = self.driver.find_elements_by_xpath("//li[contains(@class,'x-boundlist-item')]")
        calendar = random.choice(calendar_list)
        self.calendar = calendar.get_attribute('innerHTML')
        ActionChains(self.driver).double_click(calendar).perform()
        wait_until_extjs(self.driver, 10)

        plan_form.find_element_by_xpath("//input[@name='AssociatedTaskId']/ancestor::tr//div[@role='button']").click()
        time.sleep(1)
        task_list = self.driver.find_elements_by_xpath("//li[contains(@class,'x-boundlist-item')]")
        task_list = list(set(task_list) - set(calendar_list))
        task = random.choice(task_list)
        self.task = task.get_attribute('innerHTML')
        ActionChains(self.driver).move_to_element(task).double_click(task).perform()
        wait_until_extjs(self.driver, 10)


class EditPlanView(BaseView):
    def __init__(self, driver):
        BaseView.__init__(self, driver)
        wait_until_url_contains(self.driver, 10, 'EditPlan')
        wait_until_extjs(self.driver, 10)

    def save_plan(self):
        pass

    def get_info(self):
        pass

    def plan_information_is_ok(self):
        pass

    def close(self):
        pass