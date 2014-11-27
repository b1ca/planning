# coding=utf-8
from __future__ import unicode_literals
import time
from helpers.plan import Plan
from views.base_view import BaseView
from helpers.waits import wait_until_extjs, wait_until_url_contains


class PlansListView(BaseView):
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


class EditPlanView(BaseView):
    def __init__(self, driver):
        BaseView.__init__(self, driver)
        wait_until_url_contains(self.driver, 10, 'EditPlan')
        wait_until_extjs(self.driver, 10)

    def save_plan(self):
        pass

    def change_plan(self):
        info_form = self.get_info_form()
        new_plan = self.current_plan
        new_plan.set_form(info_form)
        new_plan.get_calendar_and_task()
        new_plan.modify()
        new_plan.fill_form()
        BaseView.current_plan = new_plan

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
