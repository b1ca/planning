# coding=utf-8
from __future__ import unicode_literals
import time
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from selenium.webdriver import ActionChains
from helpers.plan import Plan
from views.base_view import BaseView
from helpers.waits import wait_until_extjs, wait_until_url_contains


class PlansListView(BaseView):
    def __init__(self, driver):
        BaseView.__init__(self, driver)
        wait_until_url_contains(self.driver, 10, 'PlansList')
        wait_until_extjs(self.driver, 10)

    def get_new_plan_form(self):
        self.driver.find_element_by_xpath("//span[.='Новый план']/ancestor::a").click()
        return self.get_form_by_title('Создать новый план')

    def create_new_plan(self):
        plan_form = self.get_new_plan_form()
        plan = Plan(self.driver)
        plan.set_form(plan_form)
        plan.get_calendar_and_task()
        plan.fill_form()
        BaseView.current_plan = plan
        return EditPlanView(self.driver)

    def have_changed_plan(self):
        records = self.driver.find_elements_by_xpath(
            "//div[.='%s']/ancestor::tr[contains(@id, 'record')]//div" % self.current_plan.title)
        result = [
            records[2].text == self.current_plan.title,
            records[3].text == self.current_plan.description,
            self.current_plan.task.startswith(records[5].text),
        ]
        print result
        return all(result)

    def navigate_edit_plan_view(self):
        t = self.current_plan.title
        edit_btn = self.driver.find_element_by_xpath(
            "//div[.='%s']/ancestor::tr[contains(@id, 'record')]//img[contains(@class,'edit')][@role='button']" % t)
        ActionChains(self.driver).move_to_element(edit_btn).click(edit_btn).perform()
        self.click_go_btn_warning()
        return EditPlanView(self.driver)

    def click_go_btn_warning(self):
        self.driver.find_element_by_xpath(
            "//div[contains(@class, 'x-message-box')]//span[.='Перейти к редактированию']/ancestor::a").click()
        wait_until_extjs(self.driver, 10)


class EditPlanView(BaseView):
    def __init__(self, driver):
        BaseView.__init__(self, driver)
        wait_until_url_contains(self.driver, 10, 'EditPlan')
        wait_until_extjs(self.driver, 10)

    def save_plan(self):
        edit_plan_save_btn = lambda driver: driver.find_element_by_xpath(
            "//span[contains(@class, 'edit-plan-save-btn')]/ancestor::a")
        try:
            edit_plan_save_btn(self.driver).click()
            self.click_save_btn_warning()
        except NoSuchElementException:
            edit_plan_save_btn(self.driver).click()
            self.click_save_btn_warning()
        wait_until_extjs(self.driver, 10)

    def change_plan(self):
        info_form = self.get_info_form()
        new_plan = self.current_plan
        new_plan.set_form(info_form)
        new_plan.get_calendar_and_task()
        new_plan.modify()
        new_plan.fill_form()
        BaseView.current_plan = new_plan
        self.click_save_btn_warning()
        self.click_ok_btn_info()
        wait_until_extjs(self.driver, 10)

    def get_info_form(self):
        self.driver.find_element_by_css_selector('a[data-qtip="Информация о плане"]').click()
        time.sleep(1)
        return self.get_form_by_title('Информация о плане')

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

    def close_not_saved_and_save(self):
        close_btn = lambda driver: driver.find_element_by_css_selector('span.x-tab-close-btn')
        try:
            close_btn(self.driver).click()
            self.click_save_plan_btn_on_close()
        except ElementNotVisibleException:
            close_btn(self.driver).click()
            self.click_save_plan_btn_on_close()
        return PlansListView(self.driver)

    def click_save_btn_warning(self):
        self.driver.find_element_by_xpath(
            "//div[contains(@class, 'x-message-box')]//span[.='Сохранить']/ancestor::a").click()
        wait_until_extjs(self.driver, 10)

    def click_ok_btn_info(self):
        self.driver.find_element_by_xpath("//div[contains(@class, 'x-message-box')]//span[.='OK']/ancestor::a").click()
        wait_until_extjs(self.driver, 10)

    def click_save_plan_btn_on_close(self):
        self.driver.find_element_by_xpath("//div[contains(@class, 'x-message-box')]//span[.='Да']/ancestor::a").click()
        wait_until_extjs(self.driver, 10)
