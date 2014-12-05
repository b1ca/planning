# coding=utf-8
from __future__ import unicode_literals
from helpers.waits import wait_until_url_contains, wait_until_extjs
from views.base_view import BaseView
import random
import time


class ARMView(BaseView):
    def __init__(self, driver):
        BaseView.__init__(self, driver)
        wait_until_url_contains(self.driver, 10, 'ArmApp')
        wait_until_extjs(self.driver, 10)
        self.report_title = 'report_title_%s' % str(int(round(time.time() * 1000)))

    def create_report(self, report_type):
        time.sleep(1)
        self.driver.find_element_by_xpath("//span[.='%s']/ancestor::a" % report_type).click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//span[.='Далее']/ancestor::a").click()
        wait_until_url_contains(self.driver, 10, 'Report')
        reports = self.driver.find_elements_by_xpath("//img[contains(@data-qtip,'обавить в отчет')]")[:10]
        report = random.choice(reports)
        report.click()
        time.sleep(1)
        self.driver.find_element_by_xpath("//span[.='Сохранить']/ancestor::a").click()
        self.driver.find_element_by_xpath("//input[@name='Title']").send_keys(self.report_title)
        self.driver.find_element_by_xpath("//textarea[@name='Description']").send_keys('cool description')
        self.driver.find_elements_by_xpath("//span[.='Сохранить']/ancestor::a")[-1].click()
        self.driver.find_element_by_xpath("//span[.='Перейти в список отчетов']/ancestor::a").click()
        wait_until_url_contains(self.driver, 10, 'ReportsList')
        self.driver.find_element_by_xpath("//span[.='OK']/ancestor::a").click()

    def publish_report(self):
        self.driver.find_element_by_xpath(
            "//div[.='%s']/ancestor::tr/td[contains(@class, 'publish_column')]//span" % self.report_title).click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//span[.='Опубликовать']/ancestor::a").click()
        self.driver.find_element_by_xpath("//span[.='Да']/ancestor::a").click()
        wait_until_extjs(self.driver, 10)
        self.driver.find_element_by_xpath("//span[.='OK']/ancestor::a").click()

    def unpublish_report(self):
        yes_btn_xpath = "(//div/ancestor::tr/td[contains(@class, 'publish_column')]//span[.='Да'])[1]"
        yes_btn = self.driver.find_element_by_xpath(yes_btn_xpath)
        self.report_title = yes_btn.find_element_by_xpath(
            "%s/ancestor::tr/td[3]" % yes_btn_xpath).get_attribute('data-qtip')
        yes_btn.click()
        self.driver.find_element_by_xpath("//span[.='Да']/ancestor::a").click()
        wait_until_extjs(self.driver, 10)
        self.driver.find_element_by_xpath("//span[.='OK']/ancestor::a").click()

    def report_published(self):
        time.sleep(1)
        return 'Да' in self.driver.find_element_by_xpath(
            "//div[.='%s']/ancestor::tr/td[contains(@class, 'publish_column')]//span" % self.report_title).text

    def report_unpublished(self):
        time.sleep(1)
        return 'Нет' in self.driver.find_element_by_xpath(
            "//div[.='%s']/ancestor::tr/td[contains(@class, 'publish_column')]//span" % self.report_title).text