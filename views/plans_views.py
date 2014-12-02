# coding=utf-8
from __future__ import unicode_literals
import os
import time
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from selenium.webdriver import ActionChains
from helpers.plan import Plan
from helpers.task import ChangedTask
from views.archive_view import ArchiveView
from views.base_view import BaseView
from helpers.waits import wait_until_extjs, wait_until_url_contains
from views.monitoring_view import MonitoringView


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

    def navigate_edit_plan_view(self, title=None):
        t = title or self.current_plan.title
        edit_btn = self.driver.find_element_by_xpath(
            "//div[.='%s']/ancestor::tr[contains(@id, 'record')]//img[contains(@class,'edit')][@role='button']" % t)
        ActionChains(self.driver).move_to_element(edit_btn).click(edit_btn).perform()
        self.click_go_btn_warning()
        return EditPlanView(self.driver)

    def click_go_btn_warning(self):
        self.driver.find_element_by_xpath(
            "//div[contains(@class, 'x-message-box')]//span[contains(.,'Перейти ')]/ancestor::a |"
            "//div[contains(@class, 'x-message-box')]//span[contains(.,'Переместить в')]/ancestor::a").click()
        wait_until_extjs(self.driver, 10)

    def navigate_view_plan_view(self, title=None):
        wait_until_extjs(self.driver, 10)
        t = title or self.current_plan.title
        btn_xpath = "//div[.='%s']/ancestor::tr[contains(@id, 'record')]//img[contains(@class,'%s')][@role='button']"
        archive_btn = self.driver.find_element_by_xpath(btn_xpath % (t, 'archive'))
        view_btn = self.driver.find_element_by_xpath(btn_xpath % (t, 'view'))
        ActionChains(self.driver).move_to_element(archive_btn).click(view_btn).perform()
        self.click_go_btn_warning()
        return ViewPlanView(self.driver)

    def move_plan_to_archive(self, title=None):
        wait_until_extjs(self.driver, 10)
        t = title or self.current_plan.title
        btn_xpath = "//div[.='%s']/ancestor::tr[contains(@id, 'record')]//img[contains(@class,'%s')][@role='button']"
        archive_btn = self.driver.find_element_by_xpath(btn_xpath % (t, 'archive'))
        ActionChains(self.driver).move_to_element(archive_btn).click(archive_btn).perform()
        self.click_go_btn_warning()
        return ArchiveView(self.driver)

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

    def navigate_monitoring(self):
        self.driver.find_element_by_xpath("//span[contains(@class, 'monitoring-report')]/ancestor::a").click()
        self.click_go_btn_warning()
        return MonitoringView(self.driver)

    def download_plan_is_ok(self):
        title = self.get_first_plan_title()
        self.driver.find_element_by_xpath(
            "//div[.='%s']/ancestor::tr[contains(@id, 'record')]"
            "//img[contains(@class,'mpp-plan-action')][@role='button']" % title).click()
        xml_file = str(''.join([title, '.xml']))
        xml_is_not_empty = None
        while True:
            try:
                xml_is_not_empty = os.path.getsize(xml_file) > 0
                os.remove(xml_file)
                break
            except WindowsError:
                time.sleep(1)
                continue
        return xml_is_not_empty

    def get_first_plan_title(self):
        return self.driver.find_element_by_xpath(
            "//div[contains(@id, 'PlansView')]//tr[@data-recordindex='0']/td[@data-qtip]").text


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
            self.click_ok_btn_info()
        except NoSuchElementException:
            edit_plan_save_btn(self.driver).click()
            self.click_save_btn_warning()
            self.click_ok_btn_info()
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
        wait_until_extjs(self.driver, 10)
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

    def add_task(self, number_of_tasks):
        add_task_btn = self.driver.find_element_by_xpath("//span[contains(@class, 'edit-plan-plus-btn')]/ancestor::a")
        for i in range(1, number_of_tasks+1):
            add_task_btn.click()
            wait_until_extjs(self.driver, 10)
            time.sleep(1)
            self.add_task_name(i)
            time.sleep(1)
            self.add_resource(i)
            wait_until_extjs(self.driver, 10)
            time.sleep(1)

    def add_task_name(self, i):
        name_cell = self.driver.find_element_by_xpath(
            "//tr[@data-recordindex='%s']/td[contains(@class, 'namecell')]" % str(i-1))
        ActionChains(self.driver).double_click(name_cell).perform()
        time.sleep(1)
        name_input = self.driver.find_elements_by_css_selector("input[name='Name']")[-1]
        name_input.clear()
        name_input.send_keys('_'.join(['New_Task', str(i)]))

    def add_resource(self, i):
        resource_cell = self.driver.find_element_by_xpath(
            "//tr[@data-recordindex='%s']/td[contains(@class, 'resourcecell')]" % str(i-1))
        ActionChains(self.driver).double_click(resource_cell).perform()
        wait_until_extjs(self.driver, 10)
        self.driver.find_element_by_xpath("//span[.='Избранное']/ancestor::a").click()
        long_xpath = ("//div[contains(@id, 'tabpanel')][contains(@class, 'x-window-item')]"
                      "//tr[@data-recordindex='0']"
                      "//div[@class='x-grid-cell-inner ']")
        resource = [el for el in self.driver.find_elements_by_xpath(long_xpath) if el.size]
        ActionChains(self.driver).double_click(resource[0]).perform()

    def change_task(self):
        title = self.change_title()
        resource = self.change_resource()
        start_date = self.change_start_date()
        end_date = self.change_end_date()
        BaseView.current_plan.changed_task = ChangedTask(title, resource, start_date, end_date)

    def change_title(self):
        name_cell = self.driver.find_element_by_xpath(
            "//tr[@data-recordindex='0']/td[contains(@class, 'namecell')]/div")
        title = '_'.join([name_cell.text, 'edited'])
        ActionChains(self.driver).double_click(name_cell).perform()
        name_input = self.driver.find_element_by_css_selector("input[name='Name']")
        name_input.clear()
        name_input.send_keys(title)
        self.driver.find_element_by_css_selector('.sch-simple-timeheader').click()
        time.sleep(1)
        return title

    def change_resource(self):
        resource_cell = self.driver.find_element_by_xpath(
            "//tr[@data-recordindex='0']/td[contains(@class, 'resourcecell')]/div")
        ActionChains(self.driver).double_click(resource_cell).perform()
        wait_until_extjs(self.driver, 10)
        self.driver.find_element_by_xpath("//span[.='Избранное']/ancestor::a").click()
        long_xpath = ("//div[contains(@id, 'tabpanel')][contains(@class, 'x-window-item')]"
                      "//tr[@data-recordindex='1']"
                      "//div[@class='x-grid-cell-inner ']")
        resources = [el for el in self.driver.find_elements_by_xpath(long_xpath) if el.size]
        resource = resources[0].text
        ActionChains(self.driver).double_click(resources[0]).perform()
        self.driver.find_element_by_css_selector('.sch-simple-timeheader').click()
        time.sleep(1)
        return resource

    def change_start_date(self):
        start_date_cell = self.driver.find_element_by_xpath(
            "//tr[@data-recordindex='0']/td[contains(@class, 'startdate')]/div")
        start_date_text = start_date_cell.text
        ActionChains(self.driver).move_to_element(start_date_cell).perform()
        start_date_minutes = start_date_text.split(':')[-1]
        start_date_minutes = ''.join([start_date_minutes[:-1], '4'])
        start_date = ':'.join([start_date_text.split(':')[0], start_date_minutes])
        print 'start - %s' % start_date
        ActionChains(self.driver).double_click(start_date_cell).perform()
        start_date_input = self.driver.find_element_by_xpath("//table[contains(@id, 'startdate')]//input")
        start_date_input.clear()
        start_date_input.send_keys(start_date)
        self.driver.find_element_by_css_selector('.sch-simple-timeheader').click()
        time.sleep(1)
        return start_date

    def change_end_date(self):
        end_date_cell = self.driver.find_element_by_xpath(
            "//tr[@data-recordindex='0']/td[contains(@class, 'enddate')]/div")
        end_date_text = end_date_cell.text
        ActionChains(self.driver).move_to_element(end_date_cell).perform()
        end_date_minutes = end_date_text.split(':')[-1]
        end_date_minutes = ''.join([end_date_minutes[:-1], '6'])
        end_date = ':'.join([end_date_text.split(':')[0], end_date_minutes])
        print 'end - %s' % end_date
        ActionChains(self.driver).double_click(end_date_cell).perform()
        end_date_input = self.driver.find_element_by_xpath("//table[contains(@id, 'enddate')]//input")
        end_date_input.clear()
        end_date_input.send_keys(end_date)
        self.driver.find_element_by_css_selector('.sch-simple-timeheader').click()
        time.sleep(1)
        return end_date

    def publish_plan(self):
        """
        edit_plan_view = plans_view.create_new_plan()
        edit_plan_view.add_task(number_of_tasks=1)
        edit_plan_view.save_plan()
        edit_plan_view.publish_plan()
        plans_view = edit_plan_view.close()
        """
        time.sleep(2)
        publish_btn = self.driver.find_element_by_xpath("//span[contains(@class, 'edit-plan-doc-btn')]/ancestor::a")
        publish_btn.click()
        self.click_publish_btn_warning()

    def click_publish_btn_warning(self):
        self.driver.find_element_by_xpath(
            "//div[contains(@class, 'x-message-box')]//span[.='Опубликовать']/ancestor::a").click()
        wait_until_extjs(self.driver, 5)
        self.driver.find_elements_by_xpath("//span[.='Опубликовать']/ancestor::a")[-1].click()
        wait_until_extjs(self.driver, 10)
        self.click_ok_btn_info()


class ViewPlanView(BaseView):
    def __init__(self, driver):
        BaseView.__init__(self, driver)
        wait_until_url_contains(self.driver, 10, 'ViewPlan')
        wait_until_extjs(self.driver, 10)

    def have_task(self, number_of_tasks):
        result = []
        for i in range(1, number_of_tasks+1):
            name_cell = self.driver.find_element_by_xpath(
                "//tr[@data-recordindex='%s']/td[contains(@class, 'namecell')]/div" % str(i-1))
            result.append(name_cell.text == '_'.join(['New_Task', str(i)]))
            resource_cell = self.driver.find_element_by_xpath(
                "//tr[@data-recordindex='%s']/td[contains(@class, 'resourcecell')]/div" % str(i-1))
            result.append(bool(resource_cell.text))
        print result
        return all(result)

    def have_changed_task(self):
        xpath = "//tr[@data-recordindex='0']/td[contains(@class, '%s')]/div"
        changed_task = self.current_plan.changed_task
        result = [
            self.driver.find_element_by_xpath(xpath % 'namecell').text == changed_task.title,
            changed_task.resource in self.driver.find_element_by_xpath(xpath % 'resourcecell').text,
            self.driver.find_element_by_xpath(xpath % 'startdate').text == changed_task.start_date,
            self.driver.find_element_by_xpath(xpath % 'enddate').text == changed_task.end_date
        ]
        print result
        return all(result)