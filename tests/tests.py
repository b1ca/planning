# coding=utf-8
from __future__ import unicode_literals
from base_test import BaseTest


class PlanningTestCase(BaseTest):

    def test_create_new_plan(self):  # 1) Сценарий «Создание Нового плана»
        plans_view = self.current_view.navigate_plans_list_view()
        edit_plan_view = plans_view.create_new_plan()
        assert edit_plan_view.plan_information_is_ok()
        current_view = edit_plan_view.close()
        assert '#PlansList' in current_view.driver.current_url

    def test_edit_new_plan_1_way(self):  # 2) Сценарий «Редактирования Нового плана»  - 1 способ
        plans_view = self.current_view.navigate_plans_list_view()
        edit_plan_view = plans_view.create_new_plan()
        edit_plan_view.change_plan()
        # edit_plan_view.save_btn_click()
        # edit_plan_view.close()
        # plans_view = edit_plan_view.save_plan()
        # assert plans_view.have_changed_plan()

    # def test_edit_new_plan_2_way(self):  # 3) Сценарий «Редактирования Нового плана»  - 2 способ
    #     plans_view = self.current_view.navigate_plans_list_view()
    #     edit_plan_view = plans_view.create_plan()
    #     edit_plan_view.change_plan()
    #     edit_plan_view.save_btn_click()
    #     edit_plan_view.save_plan()
    #     plans_view = edit_plan_view.navigate_plans_list_view()
    #     assert plans_view.have_changed_plan()
    #
    # def test_edit_new_plan_3_way(self):  # 4) Сценарий «Редактирования Нового плана»  - 3 способ
    #     plans_view = self.current_view.navigate_plans_list_view()
    #     edit_plan_view = plans_view.create_plan()
    #     plans_view = edit_plan_view.close()
    #     edit_plan_view = plans_view.navigate_edit_view()
    #     edit_plan_view.change_plan()
    #     edit_plan_view.save_btn_click()
    #     edit_plan_view.save_plan()
    #     plans_view = edit_plan_view.navigate_plans_list_view()
    #     assert plans_view.have_changed_plan()
    #
    # def test_add_task_to_new_plan(self):  # 5) Сценарий «Добавление задачи в новый план»
    #     pass
    #
    # def test_add_several_tasks_to_new_plan(self):  # 6) Сценарий «Добавления нескольких задач для плана»
    #     pass
    #
    # def test_edit_added_task(self):  # 7) Сценарий «Редактирования добавленной задачи в план»
    #     pass
    #
    # def test_move_plan_to_archive(self):  # 8) Сценарий «Перенос плана в архив»
    #     pass
    #
    # def test_view_plan(self):  # 9) Сценарий «Просмотр плана»
    #     pass
    #
    # def test_view_plan_through_user(self):  # 10) Сценарий «Просмотр плана через пользователя»
    #     pass
