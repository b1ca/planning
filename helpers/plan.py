# coding=utf-8
from __future__ import unicode_literals
from datetime import datetime
from selenium.common.exceptions import MoveTargetOutOfBoundsException
from selenium.webdriver import ActionChains
import time
import random
from helpers.waits import wait_until_extjs


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
        self.modified = False
        self.form = None

    def set_form(self, plan_form):
        self.form = plan_form

    def fill_form(self):
        self.fill_title_and_description()
        self.fill_date()
        if not self.modified:
            self.fill_time()
            self.click_create_btn()
        else:
            self.click_save_btn()

    def fill_title_and_description(self):
        plan_form = self.form
        title_field = plan_form.find_element_by_css_selector('input[name=Title]')
        title_field.clear()
        title_field.send_keys(self.title)
        description_field = plan_form.find_element_by_css_selector('textarea[name=Description]')
        description_field.clear()
        description_field.send_keys(self.description)

    def fill_date(self):
        plan_form = self.form
        plan_form.find_element_by_xpath("//table[contains(@id,'datefield')]//div[@role='button']").click()
        if self.modified:
            plan_form.find_element_by_xpath(
                "//td[not(contains(@class, 'disabled'))]/a[@class='x-datepicker-date'][.='%s']" % self.date).click()
        else:
            plan_form.find_element_by_xpath("//td[@title='Сегодня']/a").click()

    def fill_time(self):
        plan_form = self.form
        plan_form.find_element_by_xpath("//table[contains(@id,'timefield')]//div[@role='button']").click()
        plan_form.find_element_by_xpath("//li[contains(@class,'x-boundlist-item')][.='%s']" % self.time).click()

    def click_create_btn(self):
        self.form.find_element_by_xpath("//span[.='Создать']/ancestor::a").click()
        wait_until_extjs(self.driver, 10)

    def click_save_btn(self):
        self.form.find_element_by_xpath("//span[.='Сохранить']/ancestor::a").click()
        wait_until_extjs(self.driver, 10)

    def get_calendar_and_task(self):
        plan_form = self.form
        plan_form.find_element_by_xpath("//input[@name='CalendarId']/ancestor::tr//div[@role='button']").click()
        wait_until_extjs(self.driver, 10)
        calendar_list = self.driver.find_elements_by_xpath("//li[contains(@class,'x-boundlist-item')]")
        calendar = random.choice(calendar_list)
        self.calendar = calendar.get_attribute('innerHTML')
        ActionChains(self.driver).double_click(calendar).perform()
        wait_until_extjs(self.driver, 10)

        task_input_name = 'AssociatedTaskId' if 'EditPlan' not in self.driver.current_url else 'LinkTaskId'
        plan_form.find_element_by_xpath(
            "//input[@name='%s']/ancestor::tr//div[@role='button']" % task_input_name).click()
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

    def modify(self):
        self.title, self.description = map(lambda x: '_'.join([x, 'edited']), [self.title, self.description])
        self.date = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%d.%m.%Y')
        self.modified = True
