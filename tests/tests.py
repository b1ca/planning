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
        plans_view = edit_plan_view.close_not_saved_and_save()
        assert plans_view.have_changed_plan()

    def test_edit_new_plan_2_way(self):  # 3) Сценарий «Редактирования Нового плана»  - 2 способ
        plans_view = self.current_view.navigate_plans_list_view()
        edit_plan_view = plans_view.create_new_plan()
        edit_plan_view.change_plan()
        edit_plan_view.save_plan()
        plans_view = edit_plan_view.navigate_plans_list_view()
        assert plans_view.have_changed_plan()

    def test_edit_new_plan_3_way(self):  # 4) Сценарий «Редактирования Нового плана»  - 3 способ
        plans_view = self.current_view.navigate_plans_list_view()
        edit_plan_view = plans_view.create_new_plan()
        plans_view = edit_plan_view.close()
        edit_plan_view = plans_view.navigate_edit_plan_view()
        edit_plan_view.change_plan()
        edit_plan_view.save_plan()
        plans_view = edit_plan_view.navigate_plans_list_view()
        assert plans_view.have_changed_plan()

    def test_add_task_to_new_plan(self):  # 5) Сценарий «Добавление задачи в новый план»
        plans_view = self.current_view.navigate_plans_list_view()
        edit_plan_view = plans_view.create_new_plan()
        edit_plan_view.add_task(number_of_tasks=1)
        edit_plan_view.save_plan()
        plans_view = edit_plan_view.close()
        plan_view = plans_view.navigate_view_plan_view()
        assert plan_view.have_task(number_of_tasks=1)

    def test_add_several_tasks_to_new_plan(self):  # 6) Сценарий «Добавления нескольких задач для плана»
        plans_view = self.current_view.navigate_plans_list_view()
        edit_plan_view = plans_view.create_new_plan()
        edit_plan_view.add_task(number_of_tasks=2)
        edit_plan_view.save_plan()
        plans_view = edit_plan_view.close()
        plan_view = plans_view.navigate_view_plan_view()
        assert plan_view.have_task(number_of_tasks=2)

    def test_edit_added_task(self):  # 7) Сценарий «Редактирования добавленной задачи в план»
        plans_view = self.current_view.navigate_plans_list_view()
        edit_plan_view = plans_view.create_new_plan()
        edit_plan_view.add_task(number_of_tasks=1)
        edit_plan_view.save_plan()
        plans_view = edit_plan_view.close()
        edit_plan_view = plans_view.navigate_edit_plan_view()  # plan_title_1417419154272
        edit_plan_view.change_task()
        edit_plan_view.save_plan()
        plans_view = edit_plan_view.close()
        plan_view = plans_view.navigate_view_plan_view()
        assert plan_view.have_changed_task()

    def test_move_plan_to_archive(self):  # 8) Сценарий «Перенос плана в архив»
        plans_view = self.current_view.navigate_plans_list_view()
        edit_plan_view = plans_view.create_new_plan()
        plans_view = edit_plan_view.close()
        archive_view = plans_view.move_plan_to_archive()
        assert archive_view.have_changed_plan()

    def test_view_plan(self):  # 9) Сценарий «Просмотр плана»
        plans_view = self.current_view.navigate_plans_list_view()
        edit_plan_view = plans_view.create_new_plan()
        plans_view = edit_plan_view.close()
        current_view = plans_view.navigate_view_plan_view()
        assert '#ViewPlan' in current_view.driver.current_url

    def test_view_plan_through_user(self):  # 10) Сценарий «Просмотр плана через пользователя»
        users_view = self.current_view.navigate_users_view()
        users_view.choose_user('Немиро')
        current_view = users_view.navigate_view_plan_view()
        assert '#ViewPlan' in current_view.driver.current_url

    def test_plan_monitoring(self):  # 11) Сценарий «Мониторинг плана»
        plans_view = self.current_view.navigate_plans_list_view()
        current_view = plans_view.navigate_monitoring()
        assert 'Monitoring' in current_view.driver.current_url

    def test_download_plan_as_ms_project_xml(self):  # 12) Сценарий «Скачивание плана в формате MS Project (.XML)
        plans_view = self.current_view.navigate_plans_list_view()
        assert plans_view.download_plan_is_ok()

    def test_create_new_plan_with_template(self):  # 13) Сценарий «Создание плана из шаблона»
        plans_view = self.current_view.navigate_plans_list_view()
        edit_plan_view = plans_view.create_new_plan(from_template=True)
        plans_view = edit_plan_view.close()
        assert 'draft' or 'template' in plans_view.get_plan_type()

    # 14) Сценарий «Фильтрации Списка планов по опубликованные»
    # 15) Сценарий «Фильтрации Списка планов, показывать только шаблоны»
    # 16) Сценарий «Фильтрации Списка планов, Показывать только черновики»
    # 17) Сценарий «Фильтрации Списка планов, все планы»
    def test_filters(self):
        plans_view = self.current_view.navigate_plans_list_view()
        plans_view.show('pub')
        assert plans_view.on_page_shown('pub')
        plans_view.show('template')
        assert plans_view.on_page_shown('template')
        plans_view.show('draft')
        assert plans_view.on_page_shown('draft')
        plans_view.show('all')
        assert plans_view.on_page_shown('all')

    def test_create_and_publish_plan(self):  # 18) Сценарий Создание и публикация плана
        plans_view = self.current_view.navigate_plans_list_view()
        edit_plan_view = plans_view.create_new_plan(timedelta=5)
        edit_plan_view.add_task(number_of_tasks=1)
        edit_plan_view.save_plan()
        edit_plan_view.publish_plan()
        plans_view = edit_plan_view.close()
        assert plans_view.have_changed_plan()

    def test_add_resource_and_publish_plan(self):  # 19) Сценарий  Добавления ресурса и публикация плана
        plans_view = self.current_view.navigate_plans_list_view()
        edit_plan_view = plans_view.create_new_plan(timedelta=5)
        edit_plan_view.add_task(number_of_tasks=1)
        edit_plan_view.save_plan()
        edit_plan_view.add_resource_to_plan()
        edit_plan_view.publish_plan()
        plans_view = edit_plan_view.close()
        assert plans_view.have_changed_plan()

    def test_report_creation__tasks(self):  # 20) Сценарий Создания отчёта,  по задачам
        pass

    def test_report_creation__plan(self):  # 21) Сценарий Создания отчёта,  поплану
        pass

    def test_unpublish_report(self):  # 22) Сценарий снятии отчёта с публикации
        pass

    # 23) Создания плана с публикацией и Расширенными настройками доступа к плану.
    def test_create_and_publish_plan_with_extended_prefs(self):
        pass
