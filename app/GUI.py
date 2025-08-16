import json
import logging
import multiprocessing
import os
import threading
import time
from tkinter import Tk, ttk, messagebox, Text, Scrollbar, Toplevel

from Client import Client
from VK_API import VKFishing

class VKBotGUI(Tk):
    def apply_style(self):
        style = ttk.Style()
        style.configure("Custom.TWindow", background="white", foreground="black")
        style.configure("Custom.TButton", padding=6, font=("Arial", 10))
        style.configure("Custom.TLabel", font=("Arial", 12))
        style.configure("Custom.TEntry", font=("Arial", 12))

    def __init__(self):
        super().__init__()
        logging.info("Инициализация графического интерфейса VKBotGUI.")
        self._id_current_item = None
        self.bot = Client()
        self.monitoring_process = None
        self.title("VK Bot")
        self.geometry("600x700")
        self.apply_style()
        self.create_widgets()

        self.log_thread = threading.Thread(target=self.update_console_logs, daemon=True)
        self.log_thread.start()

    def create_widgets(self):
        logging.info("Создание элементов интерфейса.")
        self.lots_button = ttk.Button(self, text="View Lots", command=self.view_lots, width=20, style='Custom.TButton')
        self.lots_button.pack(pady=10)

        self.url_label = ttk.Label(self, text="Enter URL", style='Custom.TLabel')
        self.url_label.pack(expand=True)

        self.url_entry = ttk.Entry(self, width=20, style="Custom.TEntry")
        self.url_entry.pack(pady=10)

        self.auth_key_label = ttk.Label(self, text="Enter Access Token Key", style='Custom.TLabel')
        self.auth_key_label.pack(expand=True)

        self.auth_key_entry = ttk.Entry(self, width=20, style="Custom.TEntry")
        self.auth_key_entry.pack(pady=10)

        self.items_frame = ttk.Frame(self)
        self.items_frame.pack(pady=10)

        self.create_items_button()

        self.price_label = ttk.Label(self, text="Enter Max Price", style="Custom.TLabel")
        self.price_label.pack(pady=10)

        self.price_entry = ttk.Entry(self, width=40, style="Custom.TEntry")
        self.price_entry.pack(pady=5)

        self.delay_label = ttk.Label(self, text="Enter Delay", style="Custom.TLabel")
        self.delay_label.pack(pady=10)

        self.delay_entry = ttk.Entry(self, width=40, style="Custom.TEntry")
        self.delay_entry.pack(pady=5)

        self.refresh_connect = ttk.Button(self, text="Refresh", style="Custom.TButton",
                                          command=self.bot.refresh_connect)
        self.refresh_connect.pack(pady=10)

        self.monitor_button = ttk.Button(self, text="Monitor Item", command=self.start_monitoring, width=20,
                                         style="Custom.TButton")
        self.monitor_button.pack(pady=10)

        self.stop_button = ttk.Button(self, text="Stop", command=self.stop_monitoring, width=20, style="Custom.TButton")
        self.stop_button.pack(pady=10)

        self.fishing_button = ttk.Button(self, text="Fishing", command=self.start_fishing, width=20, style="Custom.TButton")
        self.fishing_button.pack(pady=10)

        self.stop_fishing_button = ttk.Button(self, text="Stop Fishing", command=self.stop_fishing, width=20, style="Custom.TButton")
        self.stop_fishing_button.pack(pady=10)

        # Кнопка для открытия настроек
        self.settings_button = ttk.Button(self, text="Settings", command=self.open_settings, width=20,
                                          style="Custom.TButton")
        self.settings_button.pack(pady=10)

        # Консоль для логов
        self.log_console = Text(self, width=60, wrap="word", state="disabled")
        self.log_console.pack(pady=10)

        # Скроллер для консоли
        log_scrollbar = Scrollbar(self, command=self.log_console.yview)
        log_scrollbar.pack(side="right", fill="y")
        self.log_console.config(yscrollcommand=log_scrollbar.set)

    def create_items_button(self):
        logging.info("Создание кнопок для списка элементов.")
        try:
            with open("items.json", "r") as f:
                items = json.load(f)
                for index, item in enumerate(items["items"]):
                    row = index // 3
                    self.geometry(f"{600}x{(row * 100) + 800}")
                    column = index % 3
                    item_id = item["id"]
                    title = item["title"]
                    ttk.Button(self.items_frame, text=title,
                               command=lambda args=(item_id, title): self.id_current_item(*args)).grid(row=row,
                                                                                                       column=column)
        except FileNotFoundError:
            logging.error("Файл items.json не найден.")
            messagebox.showerror("Error", "items.json not found.")
        except json.JSONDecodeError:
            logging.error("Ошибка при чтении items.json. Проверьте его содержимое.")
            messagebox.showerror("Error", "Invalid items.json format.")

    def id_current_item(self, item_id, name):
        self._id_current_item = item_id
        self._name_current_item = "_".join(name.split())
        logging.info(f"Выбран элемент с ID: {item_id} и именем {name}.")

    def start_fishing(self):
        logging.info("Попытка запуска бота для рыбалки")
        vk_token = self.auth_key_entry.get()
        if not vk_token:
            messagebox.showerror("Error", "You should enter your Access Token Key.")
            logging.warning("Не введен access токен")
            return
        self.vk_bot = VKFishing(vk_token)
        self.vk_bot.start()
        logging.info("Бот стартовал")

    def stop_fishing(self):
        logging.info("Попытка остановить бота для рыбалки")
        self.vk_bot.stop()
        logging.info("Бот остановлен")

    def start_monitoring(self):
        logging.info("Попытка запуска мониторинга.")
        user_id, auth_key = self.parse_url()
        max_price = self.price_entry.get()
        vk_token = self.auth_key_entry.get()
        if not vk_token:
            messagebox.showerror("Error", "You should enter your Access Token Key.")
            logging.warning("Не введен access токен")
            return
        if not max_price.isdigit():
            messagebox.showerror("Error", "Max Price should be a number.")
            logging.warning("Введена некорректная максимальная цена.")
            return
        if not hasattr(self, '_id_current_item'):
            messagebox.showerror("Error", "Please select an item ID.")
            logging.warning("Элемент не выбран.")
            return
        delay = self.delay_entry.get()
        if not delay.isdigit():
            messagebox.showerror("Error", "Delay should be a number.")
            logging.warning("Введена некорректная задержка.")
            return
        if int(delay) < 3 or int(delay) > 120:
            messagebox.showerror("Error", "Delay should be between 10 and 120.")
            logging.warning("Введена задержка вне допустимого диапазона.")
            return

        self.item_id = self._id_current_item
        self.name = self._name_current_item
        self.max_price = int(max_price)
        self.user_id = int(user_id)
        self.auth_key = auth_key
        self.delay = int(delay)
        self.vk_token = vk_token
        logging.info(
            f"Запуск мониторинга для Item ID: {self.item_id}, User ID: {self.user_id}, Auth Key: {self.auth_key}, "
            f"Max Price: {self.max_price}, Delay: {self.delay}.")
        self.bot.send_start_monitoring(item_id=self.item_id, max_price=self.max_price, delay=self.delay,
                                       user_id=self.user_id, name=self.name, auth_key=self.auth_key,
                                       vk_token=self.vk_token)

    def stop_monitoring(self):
        if self._id_current_item and self.url_entry.get():
            user_id, _ = self.parse_url()
            logging.info(f"Попытка остановить мониторинг для Item ID: {self._id_current_item}.")
            self.bot.send_stop_monitoring(item_id=self._id_current_item, user_id=user_id)
        else:
            messagebox.showerror("Error", "Please select an item ID and user ID.")

    def parse_url(self):
        if not self.url_entry.get().startswith("https://vip3.activeusers.ru/app.php?"):
            messagebox.showerror("Error", "Url should start with https://vip3.activeusers.ru/app.php?")
            logging.warning("Введен некорректный Url")
            return
        url_split = self.url_entry.get().replace("https://vip3.activeusers.ru/app.php?act=item&", "").split(
            "&")
        user_id = url_split[2].split("=")[1]
        auth_key = url_split[1].split("=")[1]
        return user_id, auth_key

    def open_settings(self):
        logging.info("Открытие окна настроек.")
        settings_window = Toplevel(self)
        settings_window.title("Settings")
        settings_window.geometry("300x200")

        self.ip_label = ttk.Label(settings_window, text="Server IP Address")
        self.ip_label.pack(pady=10)

        self.ip_entry = ttk.Entry(settings_window, width=30)
        self.ip_entry.insert(0, self.bot.server_ip)  # Значение по умолчанию из текущего IP
        self.ip_entry.pack(pady=10)

        save_button = ttk.Button(settings_window, text="Save", command=self.save_settings)
        save_button.pack(pady=10)

    def save_settings(self):
        ip = self.ip_entry.get()
        if ip == self.bot.server_ip:
            messagebox.showerror("Error", "Server IP hasn't changed.")
            return
        logging.info(f"Настройки сохранены, новый IP адрес сервера: {ip}")
        self.bot.update_server_ip(ip)

    def update_console_logs(self):
        """Функция для обновления консоли логов из файла."""
        last_pos = 0
        while True:
            with open("vk_bot.log", "r") as log_file:
                log_file.seek(last_pos)
                new_logs = log_file.read()
                if new_logs:
                    self.log_console.config(state="normal")  # Разрешаем редактирование Text
                    self.log_console.insert("end", new_logs)  # Добавляем новые строки
                    self.log_console.yview("end")  # Прокручиваем до конца
                    self.log_console.config(state="disabled")  # Отключаем редактирование
                    last_pos = log_file.tell()  # Сохраняем позицию последнего прочитанного места
            time.sleep(1)  # Задержка для обновления

    def view_lots(self):
        self.bot.send_view_lots()


if __name__ == "__main__":
    multiprocessing.set_start_method("spawn")  # Устанавливаем spawn
    logging.info("Запуск приложения.")

    app = VKBotGUI()
    app.mainloop()

    app.bot.stop()
    try:
        os.remove("vk_bot.log")
        os.remove("lot.db")
    except FileNotFoundError:
        logging.warning("Файлы vk_bot.log или lot.db не найдены.")
