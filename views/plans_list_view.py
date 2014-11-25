# coding=utf-8
from __future__ import unicode_literals
from datetime import datetime
from selenium.common.exceptions import MoveTargetOutOfBoundsException
from selenium.webdriver import ActionChains
from views.base_view import BaseView
from helpers.waits import wait_until_extjs, wait_until_url_contains
import time
import random


class PlansListView(BaseView):
    def get_new_plan_form(self):
        self.driver.find_element_by_xpath("//span[.='Новый план']/ancestor::a").click()
        wait_until_extjs(self.driver, 10)
        return get_form_by_title(self.driver, 'Создать новый план')

    def create_new_plan(self):
        plan_form = self.get_new_plan_form()
        plan = Plan(self.driver)
        plan.get_calendar_and_task(plan_form)
        plan.fill_form(plan_form)
        BaseView.current_plan = plan
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
        self.date = datetime.now().strftime('%d.%m.%Y')
        self.time = '23:45'

    def fill_form(self, plan_form):
        plan_form.find_element_by_css_selector('input[name=Title]').send_keys(self.title)
        plan_form.find_element_by_css_selector('textarea[name=Description]').send_keys(self.description)
        plan_form.find_element_by_xpath("//table[contains(@id,'datefield')]//div[@role='button']").click()
        plan_form.find_element_by_xpath("//td[@title='Сегодня']/a").click()
        plan_form.find_element_by_xpath("//table[contains(@id,'timefield')]//div[@role='button']").click()
        plan_form.find_element_by_xpath("//li[contains(@class,'x-boundlist-item')][.='%s']" % self.time).click()
        plan_form.find_element_by_xpath("//span[.='Создать']/ancestor::a").click()
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
        time.sleep(2)
        task_list = self.driver.find_elements_by_xpath("//li[contains(@class,'x-boundlist-item')]")
        task_list = list(set(task_list) - set(calendar_list))

        task_result = None
        while task_result is None:
            try:
                task_result = self.set_task(task_list)
            except MoveTargetOutOfBoundsException:
                pass
        wait_until_extjs(self.driver, 10)

    def set_task(self, task_list):
        task = random.choice(task_list)
        self.task = task.get_attribute('innerHTML')
        ActionChains(self.driver).move_to_element(task).double_click(task).perform()
        return True


class EditPlanView(BaseView):
    def __init__(self, driver):
        BaseView.__init__(self, driver)
        wait_until_url_contains(self.driver, 10, 'EditPlan')
        wait_until_extjs(self.driver, 10)

    def save_plan(self):
        pass

    def edit_plan(self):
        pass

    def get_info_form(self):
        self.driver.find_element_by_css_selector('a[data-qtip="Информация о плане"]').click()
        wait_until_extjs(self.driver, 20)
        return get_form_by_title(self.driver, 'Информация о плане')

    def plan_information_is_ok(self):
        info_form = self.get_info_form()
        plan = self.current_plan
        result = [
            info_form.find_element_by_css_selector('input[name=Title]').get_attribute('value') == plan.title,
            info_form.find_element_by_css_selector(
                'input[name=PlannedFinish]').get_attribute('value') == ' '.join([plan.date, plan.time]),
            info_form.find_element_by_css_selector(
                'textarea[name=Description]').get_attribute('value') == plan.description,
            info_form.find_element_by_css_selector('input[name=LinkTaskId]').get_attribute('value') == plan.task,
            info_form.find_element_by_css_selector(
                'input[name=CalendarId]').get_attribute('data-qtip') == plan.calendar,
        ]
        self.driver.find_element_by_xpath("//span[.='Закрыть']/ancestor::a").click()
        print result
        return all(result)

    def close(self):
        self.driver.find_element_by_css_selector('span.x-tab-close-btn').click()
        return PlansListView(self.driver)


def get_form_by_title(driver, title):
    return driver.find_element_by_xpath("//span[.='%s']/ancestor::div[contains(@class, 'x-window-closable')]" % title)