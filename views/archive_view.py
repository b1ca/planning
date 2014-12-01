# coding=utf-8
from __future__ import unicode_literals
import time
from base_view import BaseView
from helpers.waits import wait_until_url_contains, wait_until_extjs


class ArchiveView(BaseView):
    def __init__(self, driver):
        BaseView.__init__(self, driver)
        wait_until_url_contains(self.driver, 20, 'Archive')
        wait_until_extjs(self.driver, 10)
        time.sleep(2)

    def have_changed_plan(self):
        records = self.driver.find_elements_by_xpath(
            "//div[.='%s']/ancestor::tr[contains(@id, 'record')]//div" % self.current_plan.title)
        records = [r for r in records if r.text]
        result = [
            self.current_plan.title == records[1].text,
            self.current_plan.description == records[2].text,
            records[4].text in self.current_plan.task,
        ]
        print self.current_plan
        print result
        return all(result)