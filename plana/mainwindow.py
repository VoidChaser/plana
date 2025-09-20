# # Important:
# # You need to run the following command to generate the ui_form.py file
# #     pyside6-uic form.ui -o ui_form.py, or
# #     pyside2-uic form.ui -o ui_form.py
import sys
import webbrowser
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QSpinBox, QWidget, QInputDialog
from PySide6.QtWidgets import QPushButton, QHeaderView, QDialog, QMessageBox, QFileDialog, QTableWidgetItem, QAbstractItemView, QCheckBox
from PySide6.QtCore import QTimer
import os
import requests
import uuid
import threading
from PySide6.QtCore import Qt, QDate, QTime
from dateutil.relativedelta import relativedelta
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl
import sqlite3
import json
from datetime import date as dt_date
from datetime import time as dt_time
from datetime import datetime as dt_datetime
from ui_form import Ui_MainWindow
from ui_dialog_create import Ui_DialogCreate
from ui_dialog_period import Ui_DialogPeriod
from ui_welcome import Ui_WelcomeWindow

print("SQLite version:", sqlite3.sqlite_version)
def create_database(db_name: str) -> sqlite3.Connection:
    """Создает новую базу данных и возвращает соединение."""
    connection = sqlite3.connect(db_name)
    return connection

def open_database(db_name: str) -> sqlite3.Connection:
    """Открывает существующую базу данных и возвращает соединение."""
    connection = sqlite3.connect(db_name)
    return connection


is_authorized = False

class Welcome(QWidget):
    def __init__(self):
        super().__init__()
        self.session_id = None
        self.token = None
        self.user_data = None
        
        # resp = requests.get("https://fitfully-delectable-ray.cloudpub.ru/register_session").json()
        
        # self.session_id = resp["session_id"]
        
        self.ui = Ui_WelcomeWindow()
        self.ui.setupUi(self)

        self.ui.btnAuth.clicked.connect(self.open_auth)
        self.ui.btnSkip.clicked.connect(self.skip_auth)

        # Таймер для проверки авторизации
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_session)
        self.timer.start(2000)  # проверяем каждую секунду
        
        # Регистрируем новую сессию
        self.register_session()
        
    
    def register_session(self):
        # Можно сохранять session_id в файл, чтобы повторно использовать
        try:
            resp = requests.get("https://fitfully-delectable-ray.cloudpub.ru/register_session").json()
            self.session_id = resp["session_id"]
            print("Registered session:", self.session_id)
        except Exception as e:
            print("Failed to register session:", e)
        # resp = requests.get(f"https://fitfully-delectable-ray.cloudpub.ru/register_session").json()
        # self.session_id = resp["session_id"]
        # print("Registered session:", self.session_id)
        

    def open_auth(self):
        url = f"https://fitfully-delectable-ray.cloudpub.ru/?session_id={self.session_id}"
        webbrowser.open(url)
        # url = f"https://fitfully-delectable-ray.cloudpub.ru/?session_id={self.session_id}"
        # webbrowser.open(url)
        # webbrowser.open("https://fitfully-delectable-ray.cloudpub.ru/")  # ссылка авторизации

    def skip_auth(self):
        # global is_authorized
        # is_authorized = True  # считаем авторизацию выполненной
        self.timer.stop()
        self.open_main_window()

    def check_session(self):
        if not self.session_id:
            return
        
        # resp = requests.get(f"https://fitfully-delectable-ray.cloudpub.ru/session_status/{self.session_id}").json()
        # print(f"Session status:", resp)
        try:
            resp = requests.get(f"https://fitfully-delectable-ray.cloudpub.ru/session_status/{self.session_id}").json()
            user = resp.get("user")
            if resp.get("authorized") and user != self.user_data:
                self.user_data = user
                if user is not None:
                    print(f"Пользователь {self.user_data.get('first_name', 'Unknown')} авторизован")
                self.timer.stop()
                self.open_main_window(resp_data=self.user_data)
        except Exception as e:
            print("Failed to check session:", e)
        
            

    def open_main_window(self, resp_data=None):
        self.close()
        if resp_data is None:
            resp_data = {}
        resp_data["session_id"] = self.session_id
        self.main_window = MainWindow(data=resp_data)
        self.main_window.show()

class MainWindow(QMainWindow):
    def __init__(self, data={}):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # if self.data:
        #     print(self.data)
        self.data = data
        self.session_id = self.get_session_id()
        self.tasks = ''
        print(self.data)
        
        self.ui.label_time.setText(f'Привет, {self.data.get("first_name", "Гость")}')
        
        # Разрешаем выбирать только строки
        self.ui.table_tasks.setSelectionBehavior(QAbstractItemView.SelectRows)

        # Разрешаем выбрать только одну строку за раз
        self.ui.table_tasks.setSelectionMode(QAbstractItemView.SingleSelection)
        
        self.load_tasks()
        self.update_task_view()
        
    

        # Размер окна
        self.resize(1013, 600)

        # Устанавливаем текст на кнопках
        self.ui.btn_add.setText("+")
        self.ui.btn_settings.setText("!")

        # Авто-скейлинг заголовков таблицы
        header = self.ui.table_tasks.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.Stretch)
        header.setSectionResizeMode(5, QHeaderView.Stretch)
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)

        # Центрируем текст в ячейках таблицы
        self.ui.table_tasks.setAlternatingRowColors(True)
        self.ui.table_tasks.resizeRowsToContents()
        self.ui.table_tasks.resizeColumnsToContents()

        # Подключаем кнопки
        self.ui.btn_add.clicked.connect(self.open_create_dialog)
        self.ui.btn_settings.clicked.connect(self.open_period_dialog)
        self.ui.btn_delete.clicked.connect(self.open_delete_dialog)

        # Создаём диалоги заранее
        self.dialog_create = CreateDialog(self)
        self.dialog_period = PeriodDialog(self)
        # self.dialog_delete = DeleteDialog(self)
        

    def closeEvent(self, event):
        if self.session_id:
            try:
                requests.post(
                    "https://fitfully-delectable-ray.cloudpub.ru/logout",
                    json={"session_id": self.session_id},
                    timeout=3
                )
                print("Session logged out")
            except Exception as e:
                print("Failed to logout:", e)
        event.accept()

    # def closeEvent(self, event):
    #     if self.session_id:
    #         try:
    #             requests.post(
    #                 "https://fitfully-delectable-ray.cloudpub.ru/logout",
    #                 json={"session_id": self.session_id}
    #             )
    #             print("Session logged out")
    #         except Exception as e:
    #             print("Failed to logout:", e)
    #     event.accept()
    
    def get_session_id(self):
        """
        Возвращает session_id для текущего пользователя.
        Если в data есть session_id, используем его,
        иначе None
        """
        if self.data and "session_id" in self.data:
            return self.data["session_id"]
        return None
    
    def load_tasks(self):
        """Получение списка задач пользователя с сервера"""

        try:
            response = requests.get(
                "https://fitfully-delectable-ray.cloudpub.ru/tasks",
                params={"session_id": self.session_id},
                timeout=5
            )
            if response.status_code == 200:
                self.tasks = response.json()  # список словарей с задачами
                for t in self.tasks:
                    if "id" not in t:
                        print("ВНИМАНИЕ! Задача без id:", t)
                self.update_task_view()
            else:
                print("Ошибка при получении задач:", response.status_code, response.text)
                self.tasks = []
                self.update_task_view()
        except requests.RequestException as e:
            print("Ошибка соединения с сервером:", e)
            self.tasks = []
            self.update_task_view()


    def update_task_view(self):
        """Обновление таблицы с задачами в фиксированном порядке"""
        if not hasattr(self, "tasks") or not self.tasks:
            self.ui.label_time.setText(
                "Уведомления еще не созданы. Вы можете создать их с помощью кнопки +"
            )
            self.ui.table_tasks.setRowCount(0)
            self.ui.table_tasks.setColumnCount(0)
            return

        self.ui.label_time.setText("")  # очищаем сообщение
        res = self.tasks
        print(res)

        # Фиксированный порядок столбцов
        columns = ["title", "description", "start_date", "start_time", "end_date", "end_time"]
        russian_columns = ["Название", "Описание", "Дата старта", "Время старта", "Дата конца", "Время"]

        self.ui.table_tasks.setRowCount(len(res))
        self.ui.table_tasks.setColumnCount(len(columns))
        self.ui.table_tasks.setHorizontalHeaderLabels(russian_columns)

        for i, task in enumerate(res):
            for j, key in enumerate(columns):
                value = task.get(key, "")
                self.ui.table_tasks.setItem(i, j, QTableWidgetItem(str(value)))
                
    def insert_notification(self, connection: sqlite3.Connection, attrs: dict):
        
        '''
        Вставляет новую запись в таблицу notifications.
        
        Параметры:
            connection: sqlite3.Connection — соединение с базой
            attrs: dict — словарь с ключами:
                'name', 'description', 'begin_date', 'begin_time', 'deadline_date', 'deadline_time', completion
        '''
        cursor = connection.cursor()
        sql = """
        INSERT INTO notifications
        (name, description, begin_date, begin_time, deadline_date, deadline_time, completion)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(sql, (
            attrs.get("name"),
            attrs.get("description"),
            attrs.get("begin_date"),
            attrs.get("begin_time"),
            attrs.get("deadline_date"),
            attrs.get("deadline_time"),
            attrs.get("completion")
            
        ))
        connection.commit()
        print(f"Уведомление '{attrs.get('name')}' успешно добавлено!")
        
    def open_create_dialog(self):
        '''Создаем диалоговое окно -- 
        для создания увдеомления'''
        self.dialog_create.exec()
        self.update_task_view()
        
    def open_period_dialog(self):
        selected_indexes = self.ui.table_tasks.selectionModel().selectedRows()
        if not selected_indexes:
            QMessageBox.warning(self, "Внимание", "Выберите задачу для настройки уведомлений")
            return

        row = selected_indexes[0].row()
        task_data = self.tasks[row]  # берём словарь задачи
        task_id = task_data.get("task_id")
        if not task_id:
            QMessageBox.critical(self, "Ошибка", "Выбранная задача не имеет ID")
            return

        self.dialog_period.load_task(task_data)  # передаем весь словарь задачи
        self.dialog_period.exec()
        
    def open_delete_dialog(self):
        selected_indexes = self.ui.table_tasks.selectionModel().selectedRows()
        if not selected_indexes:
            QMessageBox.warning(self, "Внимание", "Выберите задачу для удаления")
            return

        row = selected_indexes[0].row()
        task_data = self.tasks[row]  # берём словарь задачи
        task_id = task_data.get("task_id")
        if not task_id:
            QMessageBox.critical(self, "Ошибка", "Выбранная задача не имеет ID")
            return
        dialog = DeleteDialog(task_data, parent=self)
        dialog.exec()
        self.load_tasks()
        self.update_task_view()
        
        
class CreateDialog(QDialog):
    """Диалог создания уведомления"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_DialogCreate()
        self.ui.setupUi(self)

        # Подключаем обработчики
        self.ui.OkCreationPushButton.clicked.connect(self.ok_pressed)
        self.ui.CancelCreationPushButton.clicked.connect(self.on_cancel)
        self.ui.DatePickCheckBox.toggled.connect(self.on_date_checkbox_toggled)

        # Инициализация календаря и формы
        self.date_pick_initiate()
        self.reset_form()

    def ok_pressed(self):
        """Обработчик кнопки подтверждения создания уведомления"""
        try:
            attrs = take_all_attributes_on_confirm(self)

            name = self.ui.NotificationNameLineEdit.text()
            description = self.ui.NotificationDescriptionTextEdit.toPlainText()
            start_date = self.ui.BeginDateCalendar.selectedDate().toPython()
            deadline = self.ui.DeadlineDateCalendar.selectedDate().toPython()

            if not name:
                raise ValueError("Введите имя уведомления!")
            if not start_date:
                raise ValueError("Выберите дату начала события!")
            if not deadline:
                raise ValueError("Выберите дату окончания события!")
            if start_date > deadline:
                raise ValueError("Дата начала события не может быть позже окончания!")

            result = self.show_confirmation_dialog(attrs)
            if result != QMessageBox.Ok:
                return

            main_window = self.parent()  # ссылка на MainWindow

            task_attrs = {
                "session_id": main_window.session_id,
                "title": attrs.get("name"),
                "description": attrs.get("description"),
                "start_date": attrs.get("begin_date"),
                "start_time": attrs.get("begin_time"),
                "end_date": attrs.get("deadline_date"),
                "end_time": attrs.get("deadline_time")
            }

            # Отправка POST запроса на сервер
            response = requests.post(
                "https://fitfully-delectable-ray.cloudpub.ru/tasks",
                json=task_attrs,
                timeout=5
            )
            if response.status_code == 200 or response.status_code == 201:
                print("Задача успешно создана:", response.json())
                # После успешного создания обновляем таблицу задач в MainWindow
                main_window.load_tasks()
                self.accept()
                self.reset_form()
            else:
                self.ui.line_exeption.setText(
                    f"Ошибка при создании задачи: {response.status_code} {response.text}"
                )

        except ValueError as e:
            self.ui.line_exeption.setText(str(e))
        except requests.RequestException as e:
            self.ui.line_exeption.setText(f"Ошибка соединения с сервером: {e}")

            
    def on_cancel(self):
        '''Обработчик: Нажата кнопка отмены.'''
        self.reset_form()
        self.reject()
                
    def show_confirmation_dialog(self, attrs):
        '''Обработчик: Создание диалога подтверждения создания уведомления с трассировкой значений.'''
        msg = QMessageBox(self)
        msg.setWindowTitle("Подтверждение уведомления")
        msg.setText("Пожалуйста, проверьте данные уведомления:")
        text = f"Имя: {attrs['name']}\nОписание: {attrs['description']}\n" \
            f"Старт: {attrs['begin_date']} {attrs['begin_time']}\n" \
            f"Дедлайн: {attrs['deadline_date']} {attrs['deadline_time']}\n"
        msg.setInformativeText(text)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Ok)
        # exec() блокирует диалог до нажатия OK или Cancel
        return msg.exec()

        
        # TODO: Добавить время в форму.


    def date_pick_initiate(self):
        '''Инициализатор: При инициализации формы -- по умолчанию
        выключен выбор времени -- скрывает layout выбора времени '''
        self.date_layout_do_unvisible()
        
        
    def reset_form(self):
        '''Инициализатор: После подтверждения формы приводит ее к виду по умолчанию.'''
        # Строки
        self.ui.NotificationNameLineEdit.setText("")
        self.ui.NotificationDescriptionTextEdit.setText("")
        
        # Чекбоксы
        self.ui.DatePickCheckBox.setChecked(False)
        
        self.reset_dates_edits()
        
    


    def reset_dates_edits(self):
        '''Иницализатор: после подтверждения формы приводит объекты дат к виду по умолчанию.'''
        # Время
        self.ui.BeginTimeEdit.setTime(QTime.currentTime())
        self.ui.DeadlineTimeEdit.setTime(QTime(23, 59, 0))
        
        # Дата
        today = QDate.currentDate()
        self.ui.BeginDateEdit.setDate(today)
        self.ui.DeadlineDateEdit.setDate(today)
        
        # Календари синхронизируем
        self.ui.BeginDateCalendar.setSelectedDate(today)
        self.ui.DeadlineDateCalendar.setSelectedDate(today)

        # Очистка ошибок
        self.ui.line_exeption.setText("")

        # Подключаем синхронизацию: если поменяли Edit, меняется Calendar
        self.ui.BeginDateEdit.dateChanged.connect(self.ui.BeginDateCalendar.setSelectedDate)
        self.ui.DeadlineDateEdit.dateChanged.connect(self.ui.DeadlineDateCalendar.setSelectedDate)

        # И если меняем календарь вручную, Edit тоже обновляем
        self.ui.BeginDateCalendar.selectionChanged.connect(
            lambda: self.ui.BeginDateEdit.setDate(self.ui.BeginDateCalendar.selectedDate())
        )
        self.ui.DeadlineDateCalendar.selectionChanged.connect(
            lambda: self.ui.DeadlineDateEdit.setDate(self.ui.DeadlineDateCalendar.selectedDate())
        )

        
    
    

    def on_date_checkbox_toggled(self, checked: bool):
        '''Обработчик: Когда состояние чекбокса "указать время" -- меняется, 
        Обработать соотв. события. -- вкл - показать, выкл -- скрыть.'''
        date_pick_checkbox = self.ui.DatePickCheckBox
        date_pick_checkbox_state = date_pick_checkbox.checkState()
        print(date_pick_checkbox_state)
        print(type(date_pick_checkbox_state))
        print(date_pick_checkbox_state.value)
        self.reset_dates_edits()
        if checked:
            self.ui.line_exeption.setText("Выбор даты включён.")
            self.date_layout_do_visible()
        else:
            
            self.ui.line_exeption.setText("Выбор даты выключен.")
            self.date_layout_do_unvisible()
        
        
    def date_layout_do_visible(self):
        '''Инициализатор -- показывает лейаут выбора даты'''
        date_layout = self.ui.DateLayout
        set_layout_visible(date_layout, visible=True)
    
    def date_layout_do_unvisible(self):
        '''Инициализатор -- скрывает лейаут выбора даты'''
        date_layout = self.ui.DateLayout
        set_layout_visible(date_layout, visible=False)

def take_all_attributes_on_confirm(self):
    '''Общая процедура -- собирает: словарь атрибутов
    Выдаёт: словарь атрибутов.'''
    on_confirm_attributes = {
    "begin_time": humanized_time(self.ui.BeginTimeEdit.time()),
    "deadline_time": humanized_time(self.ui.DeadlineTimeEdit.time()),
    "begin_date": humanized_date(self.ui.BeginDateEdit.date()),
    "deadline_date": humanized_date(self.ui.DeadlineDateEdit.date()),
    "name": self.ui.NotificationNameLineEdit.text(),
    "description": self.ui.NotificationDescriptionTextEdit.toPlainText(),
    "completion": None
    }
    # print(on_confirm_attributes)
    return on_confirm_attributes

def humanized_time(qt_time: QTime) -> str:
    # Преобразуем QTime в datetime.time
    py_time = dt_time(qt_time.hour(), qt_time.minute(), qt_time.second())
    # Форматируем в строку
    formatted_time = py_time.strftime("%H:%M")
    return formatted_time

def humanized_date(qt_date: QDate) -> str:
    # Преобразуем QDate в datetime.date
    py_date = dt_date(qt_date.year(), qt_date.month(), qt_date.day())
    # Форматируем в строку "ДД.ММ.ГГГГ"
    formatted_date = py_date.strftime("%d.%m.%Y")
    return formatted_date
    
def set_layout_visible(layout, visible: bool):
    '''
    Показывает или скрывает все виджеты внутри лейаута (рекурсивно).
    '''
    for i in range(layout.count()):
        item = layout.itemAt(i)

        if item.widget():
            item.widget().setVisible(visible)

        elif item.layout():
            set_layout_visible(item.layout(), visible)


class DeleteDialog(QDialog):
    def __init__(self, task_data, parent=None):
        super().__init__(parent)
        self.task_data = task_data
        self.task_id = task_data.get("task_id")
        self.parent_window = parent

        self.setWindowTitle("Удаление задачи")
        self.setMinimumWidth(300)

        layout = QVBoxLayout(self)

        title = task_data.get("title", "Без названия")
        label = QLabel(f"Вы уверены, что хотите удалить задачу:\n«{title}»?")
        label.setWordWrap(True)
        layout.addWidget(label)

        button_layout = QHBoxLayout()
        btn_delete = QPushButton("Удалить")
        btn_cancel = QPushButton("Отмена")
        button_layout.addWidget(btn_delete)
        button_layout.addWidget(btn_cancel)
        layout.addLayout(button_layout)

        btn_delete.clicked.connect(self.delete_task)
        btn_cancel.clicked.connect(self.reject)

    def delete_task(self):
        if not self.task_id:
            QMessageBox.critical(self, "Ошибка", "Выбранная задача не имеет ID")
            return

        try:
            response = requests.delete(
                f"https://fitfully-delectable-ray.cloudpub.ru/tasks/{self.task_id}",
                params={"session_id": getattr(self.parent_window, 'session_id', None)},
                timeout=5
            )
            if response.status_code == 200:
                QMessageBox.information(self, "Успех", "Задача успешно удалена")
                if hasattr(self.parent_window, "refresh_tasks"):
                    self.parent_window.refresh_tasks()
                self.accept()
            else:
                QMessageBox.critical(self, "Ошибка сервера", f"{response.status_code}: {response.text}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка запроса", str(e))



class PeriodDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_DialogPeriod()
        self.ui.setupUi(self)

        self.task_id = None
        self.prev_via_tg = False

        self.fixed_units = ["минут", "часов", "дней", "недель", "месяцев"]
        self.fixed_blocks = []

        self.ui.btn_confirm.clicked.connect(self.confirm)
        self.ui.checkbox_tg.setEnabled(False)
        self.update_auth_label()
        self.init_fixed_blocks()

    # ------------------- Фиксированные блоки -------------------
    def init_fixed_blocks(self):
        """Создаем фиксированные блоки уведомлений"""
        for unit in self.fixed_units:
            block_widget = QWidget()
            layout = QHBoxLayout(block_widget)

            label = QLabel(f"Напоминать каждые {unit}:")
            spinbox = QSpinBox()
            spinbox.setRange(1, 1000)
            spinbox.setValue(1)

            checkbox = QCheckBox("Активно")
            checkbox.setChecked(unit == "дней")  # по умолчанию день включён

            layout.addWidget(label)
            layout.addWidget(spinbox)
            layout.addWidget(checkbox)

            self.ui.dynamicFieldsLayout.addWidget(block_widget)

            self.fixed_blocks.append({
                "unit": unit,
                "widget": block_widget,
                "spinbox": spinbox,
                "checkbox": checkbox
            })

    # ------------------- Загрузка задачи -------------------
    def load_task(self, task_data):
        self.task_id = task_data.get("task_id")
        if not self.task_id:
            QMessageBox.critical(self, "Ошибка", "Выбранная задача не имеет ID")
            return

        # Загружаем базовую информацию
        self.ui.NameLabel.setText(task_data.get("title", ""))
        self.ui.BeginDateLabel.setText(task_data.get("start_date", ""))
        self.ui.BeginTimeLabel.setText(task_data.get("start_time", ""))
        self.ui.DeadlineDateLabel.setText(task_data.get("end_date", ""))
        self.ui.DeadlineTimeLabel.setText(task_data.get("end_time", ""))

        try:
            begin_dt = dt_datetime.strptime(
                f"{task_data.get('start_date')} {task_data.get('start_time')}", "%d.%m.%Y %H:%M"
            )
            end_dt = dt_datetime.strptime(
                f"{task_data.get('end_date')} {task_data.get('end_time')}", "%d.%m.%Y %H:%M"
            )
            self.ui.DifferenceLabel.setText(self.precise_diff(end_dt, begin_dt))
        except Exception:
            self.ui.DifferenceLabel.setText("")

        # ----------------- Загружаем уведомления -----------------
        notifications = []
        try:
            response = requests.get(
                f"https://fitfully-delectable-ray.cloudpub.ru/tasks/{self.task_id}/notifications",
                params={"session_id": self.parent().session_id},
                timeout=5
            )
            if response.status_code == 200:
                notifications = response.json()
                print("Notifications from server:", notifications)
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить уведомления: {e}")

        # ----------------- Обновляем флаг Telegram -----------------
        self.prev_via_tg = any(n.get("via_tg") for n in notifications) if notifications else False
        self.ui.checkbox_tg.setChecked(self.prev_via_tg)

        # ----------------- Проставляем фиксированные блоки -----------------
        # Сброс всех блоков
        for block in self.fixed_blocks:
            block["checkbox"].setChecked(False)
            block["spinbox"].setValue(1)

        # Если уведомлений нет — активируем день
        if not notifications:
            for block in self.fixed_blocks:
                if block["unit"] == "дней":
                    block["checkbox"].setChecked(True)
            return

        # Иначе обновляем блоки по уведомлениям
        for n in notifications:
            for block in self.fixed_blocks:
                if block["unit"] == n.get("unit"):
                    block["checkbox"].setChecked(True)
                    block["spinbox"].setValue(n.get("amount", 1))

    # ------------------- Авторизация -------------------
    def update_auth_label(self):
        main = self.parent()
        self.is_authorized = bool(main and getattr(main, "session_id", None))
        self.ui.checkbox_tg.setEnabled(self.is_authorized)
        self.ui.label_auth.setText(
            "Авторизация: Пройдена" if self.is_authorized else "Авторизация: Не пройдена"
        )
        self.ui.label_auth.setStyleSheet("color: green;" if self.is_authorized else "color: red;")
        self.ui.btn_auth.setVisible(not self.is_authorized)

    # ------------------- Сбор данных -------------------
    def collect_reminders(self):
        reminders = []
        for block in self.fixed_blocks:
            if block["checkbox"].isChecked():
                reminders.append((block["spinbox"].value(), block["unit"]))
        return reminders

    # ------------------- Подтверждение -------------------
    def confirm(self):
        if not self.task_id:
            QMessageBox.critical(self, "Ошибка", "Task ID не задан")
            return

        reminders = self.collect_reminders()
        current_via_tg = self.ui.checkbox_tg.isChecked()

        if not reminders and current_via_tg == self.prev_via_tg:
            QMessageBox.warning(self, "Внимание", "Не добавлено ни одного правила напоминания!")
            return

        payload = {
            "session_id": self.parent().session_id,
            "notifications": [{"amount": r[0], "unit": r[1], "via_tg": int(current_via_tg)} for r in reminders]
        }

        try:
            # Отправляем на сервер
            url = f"http://127.0.0.1:8000/tasks/{self.task_id}/notifications"
            r = requests.put(url, json=payload, timeout=5)
            if r.status_code != 200:
                QMessageBox.critical(self, "Ошибка сервера", f"{r.status_code}: {r.text}")
                return

            QMessageBox.information(self, "Успех", "Напоминания успешно обновлены")
            self.prev_via_tg = current_via_tg
            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка запроса", str(e))

    # ------------------- Разница дат -------------------
    def precise_diff(self, date1, date2):
        if date2 < date1:
            date1, date2 = date2, date1
        rd = relativedelta(date2, date1)
        parts = []
        if rd.years: parts.append(f"{rd.years} лет(год(а))")
        if rd.months: parts.append(f"{rd.months} месяцев(а)")
        if rd.days: parts.append(f"{rd.days} день(дня)")
        if rd.hours: parts.append(f"{rd.hours} часа(ов)")
        if rd.minutes: parts.append(f"{rd.minutes} минута(ы)")
        return " ".join(parts) if parts else "0 минут"


# class PeriodDialog(QDialog):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.ui = Ui_DialogPeriod()
#         self.ui.setupUi(self)

#         self.task_id = None
#         self.current_task_loaded = None
#         self.reminders_cache = []
#         self.is_authorized = False
#         self.prev_via_tg = False

#         self.ui.btn_confirm.clicked.connect(self.confirm)
#         self.ui.checkbox_tg.setEnabled(False)
#         self.update_auth_label()
#         self.clear_dynamic_fields()

#     # ---------------- Динамические блоки -----------------
#     def clear_dynamic_fields(self):
#         for i in reversed(range(self.ui.dynamicFieldsLayout.count())):
#             item = self.ui.dynamicFieldsLayout.itemAt(i)
#             w = item.widget()
#             if w:
#                 w.deleteLater()

#     def choose_period_type(self):
#         items = ["год", "месяц", "день", "час"]
#         item, ok = QInputDialog.getItem(self, "Выбор периода", "Что добавить?", items, 0, False)
#         return item if ok and item else None

#     def add_field_block(self, ask=True, period_type=None, amount=1):
#         if ask:
#             period_type = self.choose_period_type()
#             if not period_type:
#                 return
#         else:
#             period_type = period_type or "день"

#         options = ["минут", "часов", "дней", "месяцев", "лет"]
#         map_to_option = {"год": "лет", "месяц": "месяцев", "день": "дней", "час": "часов"}
#         default_option = map_to_option.get(period_type, "дней")

#         block_widget = QWidget()
#         block_layout = QHBoxLayout(block_widget)

#         label = QLabel("Напоминать каждые:")
#         spinbox = QSpinBox()
#         spinbox.setRange(1, 1000)
#         spinbox.setValue(amount)

#         combobox = QComboBox()
#         combobox.addItems(options)
#         idx = combobox.findText(default_option)
#         if idx >= 0:
#             combobox.setCurrentIndex(idx)

#         btn_add = QPushButton("+")
#         btn_add.setToolTip("Добавить ещё правило")
#         btn_add.clicked.connect(lambda: self.add_field_block(ask=True))

#         btn_remove = QPushButton("−")
#         btn_remove.setToolTip("Удалить это правило")
#         btn_remove.clicked.connect(lambda: self.remove_block(block_widget))

#         block_layout.addWidget(label)
#         block_layout.addWidget(spinbox)
#         block_layout.addWidget(combobox)
#         block_layout.addWidget(btn_add)
#         block_layout.addWidget(btn_remove)

#         self.ui.dynamicFieldsLayout.addWidget(block_widget)

#     def remove_block(self, widget):
#         widget.deleteLater()
#         self.reminders_cache = [
#             (amt, unit) for i, (amt, unit) in enumerate(self.reminders_cache)
#             if self.ui.dynamicFieldsLayout.itemAt(i) and self.ui.dynamicFieldsLayout.itemAt(i).widget() != widget
#         ]

#     # ------------------- Загрузка задачи -------------------
#     def load_task(self, task_data):
#         self.task_id = task_data.get("task_id")
#         if not self.task_id:
#             QMessageBox.critical(self, "Ошибка", "Выбранная задача не имеет ID")
#             return

#         # ---------------- Загружаем базовую информацию ----------------
#         self.ui.NameLabel.setText(task_data.get("title", ""))
#         self.ui.BeginDateLabel.setText(task_data.get("start_date", ""))
#         self.ui.BeginTimeLabel.setText(task_data.get("start_time", ""))
#         self.ui.DeadlineDateLabel.setText(task_data.get("end_date", ""))
#         self.ui.DeadlineTimeLabel.setText(task_data.get("end_time", ""))

#         try:
#             begin_dt = dt_datetime.strptime(
#                 f"{task_data.get('start_date')} {task_data.get('start_time')}", "%d.%m.%Y %H:%M"
#             )
#             end_dt = dt_datetime.strptime(
#                 f"{task_data.get('end_date')} {task_data.get('end_time')}", "%d.%m.%Y %H:%M"
#             )
#             self.ui.DifferenceLabel.setText(self.precise_diff(end_dt, begin_dt))
#         except Exception:
#             self.ui.DifferenceLabel.setText("")

#         # ---------------- Загружаем уведомления ----------------
#         notifications = []
#         try:
#             response = requests.get(
#                 f"http://127.0.0.1:8000/tasks/{self.task_id}/notifications",
#                 params={"session_id": self.parent().session_id},
#                 timeout=5
#             )
#             if response.status_code == 200:
#                 notifications = response.json()
#                 print("Notifications from server:", notifications)
#         except Exception as e:
#             QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить уведомления: {e}")

#         # ---------------- Обновляем флаг Telegram ----------------
#         self.prev_via_tg = any(n.get("via_tg") for n in notifications) if notifications else False
#         self.ui.checkbox_tg.setChecked(self.prev_via_tg)

#         # ---------------- Обновляем динамические блоки ----------------
#         self.clear_dynamic_fields()
#         self.current_task_loaded = self.task_id

#         # Уникальные блоки по (amount, unit)
#         unique_reminders = []
#         seen = set()
#         for n in notifications:
#             key = (n.get("amount", 1), n.get("unit", "дней"))
#             if key not in seen:
#                 unique_reminders.append(key)
#                 seen.add(key)

#         self.reminders_cache = unique_reminders.copy()

#         for amount, unit in unique_reminders:
#             self.add_field_block(ask=False, period_type=unit, amount=amount)


#     # ------------------- Авторизация -------------------
#     def auth_tg_bot(self):
#         self.is_authorized = True
#         self.update_auth_label()

#     def update_auth_label(self):
#         main = self.parent()
#         self.is_authorized = bool(main and getattr(main, "session_id", None))
#         self.ui.checkbox_tg.setEnabled(self.is_authorized)
#         self.ui.label_auth.setText(
#             "Авторизация: Пройдена" if self.is_authorized else "Авторизация: Не пройдена"
#         )
#         self.ui.label_auth.setStyleSheet("color: green;" if self.is_authorized else "color: red;")
#         self.ui.btn_auth.setVisible(not self.is_authorized)

#     # ------------------- Сбор данных -------------------
#     def collect_reminders(self):
#         reminders = []
#         for i in range(self.ui.dynamicFieldsLayout.count()):
#             w = self.ui.dynamicFieldsLayout.itemAt(i).widget()
#             if not w:
#                 continue
#             spin = w.findChild(QSpinBox)
#             combo = w.findChild(QComboBox)
#             if spin and combo:
#                 value = spin.value()
#                 text = combo.currentText()
#                 if text == "минут" and value > 59:
#                     value = 59
#                     spin.setValue(59)
#                 if text == "часов" and value > 23:
#                     value = 23
#                     spin.setValue(23)
#                 reminders.append((value, text))
#         self.reminders_cache = reminders.copy()
#         return reminders

#     # ------------------- Подтверждение -------------------
#     def confirm(self):
#         if not self.task_id:
#             QMessageBox.critical(self, "Ошибка", "Task ID не задан")
#             return

#         reminders = self.collect_reminders()  # Получаем все текущие блоки
#         current_via_tg = self.ui.checkbox_tg.isChecked()

#         # Убираем дубликаты перед отправкой
#         unique_reminders = []
#         seen = set()
#         for amount, unit in reminders:
#             key = (amount, unit)
#             if key not in seen:
#                 unique_reminders.append(key)
#                 seen.add(key)

#         try:
#             # Отправляем на сервер: сначала удаляем старые, потом создаём новые
#             url = f"http://127.0.0.1:8000/tasks/{self.task_id}/notifications"
#             payload = {
#                 "session_id": self.parent().session_id,
#                 "notifications": [{"amount": r[0], "unit": r[1], "via_tg": int(current_via_tg)} for r in unique_reminders]
#             }
#             r = requests.put(url, json=payload, timeout=5)
#             if r.status_code != 200:
#                 QMessageBox.critical(self, "Ошибка сервера", f"{r.status_code}: {r.text}")
#                 return

#             # Успешно обновлено
#             QMessageBox.information(self, "Успех", "Напоминания успешно обновлены")
#             self.prev_via_tg = current_via_tg
#             self.reminders_cache = unique_reminders.copy()  # Обновляем локальный кэш
#             self.accept()

#         except Exception as e:
#             QMessageBox.critical(self, "Ошибка запроса", str(e))



#     # ------------------- Разница дат -------------------
#     def precise_diff(self, date1, date2):
#         if date2 < date1:
#             date1, date2 = date2, date1
#         rd = relativedelta(date2, date1)
#         parts = []
#         if rd.years: parts.append(f"{rd.years} лет(год(а))")
#         if rd.months: parts.append(f"{rd.months} месяцев(а)")
#         if rd.days: parts.append(f"{rd.days} день(дня)")
#         if rd.hours: parts.append(f"{rd.hours} часа(ов)")
#         if rd.minutes: parts.append(f"{rd.minutes} минута(ы)")
#         return " ".join(parts) if parts else "0 минут"


if __name__ == "__main__":
    db = open_database('my_database.db')
    print('База данных успешно открыта!')
    db.close()
    # db = create_database('my_database.db')
    # print('База данных успешно создана!')
    # db.close()
    
    app = QApplication(sys.argv)
    # app.aboutToQuit.connect(logout_function)
    app.setStyle("Fusion")
    # window = MainWindow()
    # window.show()
    welcome = Welcome()
    welcome.show()
    sys.exit(app.exec())

