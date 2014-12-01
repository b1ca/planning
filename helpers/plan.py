# coding=utf-8
from __future__ import unicode_literals
import datetime
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
        self.date = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%d.%m.%Y')
        self.time = '18:00'
        self.modified = False
        self.form = None
        self.changed_task = None
        """
        @type changed_task: ChangedTask
        """

    def set_form(self, plan_form):
        self.form = plan_form

    def fill_form(self):
        self.fill_title_and_description()
        self.fill_date()
        if not self.modified:
            self.fill_time()
            self.click_create_plan_btn()
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
        date = self.date.split('.')[0].lstrip('0')
        plan_form.find_element_by_xpath(
            "//td[not(contains(@class, 'disabled'))]/a[@class='x-datepicker-date'][.='%s']" % date).click()

    def fill_time(self):
        wait_until_extjs(self.driver, 10)
        plan_form = self.form
        plan_form.find_element_by_xpath("//input[contains(@id,'timefield')]").send_keys(self.time)

    def click_create_plan_btn(self):
        self.form.find_element_by_xpath("//span[.='Создать']/ancestor::a").click()
        wait_until_extjs(self.driver, 10)

    def click_save_btn(self):
        self.form.find_element_by_xpath("//span[.='Сохранить']/ancestor::a[contains(@class, 'accent-button')]").click()
        wait_until_extjs(self.driver, 10)

    def get_calendar_and_task(self):
        plan_form = self.form
        plan_form.find_element_by_xpath("//input[@name='CalendarId']/ancestor::tr//div[@role='button']").click()
        wait_until_extjs(self.driver, 10)
        time.sleep(1)
        calendar_list = self.driver.find_elements_by_xpath("//li[@class='x-boundlist-item']")
        calendar = random.choice(calendar_list)
        self.calendar = calendar.get_attribute('innerHTML')
        ActionChains(self.driver).click(calendar).click(plan_form).perform()
        wait_until_extjs(self.driver, 10)

        task_input_name = 'AssociatedTaskId' if 'EditPlan' not in self.driver.current_url else 'LinkTaskId'
        plan_form.find_element_by_xpath(
            "//input[@name='%s']/ancestor::tr//div[@role='button']" % task_input_name).click()
        time.sleep(2)
        task_list = self.driver.find_elements_by_xpath("//li[@class='x-boundlist-item']")
        task_list = [t for t in task_list if ':' in t.text]

        task = random.choice(task_list[:5])
        self.task = task.get_attribute('innerHTML')
        ActionChains(self.driver).click(task).click(plan_form).perform()
        wait_until_extjs(self.driver, 10)

    def modify(self):
        self.title, self.description = map(lambda x: '_'.join([x, 'edited']), [self.title, self.description])
        self.date = (datetime.datetime.now() + datetime.timedelta(days=2)).strftime('%d.%m.%Y')
        self.modified = True
