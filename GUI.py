import json
import os
import queue
import socket
import logging
from tkinter import Tk, ttk, messagebox, Text, Scrollbar, Toplevel
import time
import threading

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,  # Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s [%(levelname)s] %(message)s",  # Формат сообщения
    handlers=[
        logging.FileHandler("vk_bot.log"),  # Логирование в файл
        logging.StreamHandler()  # Логирование в консоль
    ]
)

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

        # Поток для обновления логов в консоли
        self.log_thread = threading.Thread(target=self.update_console_logs, daemon=True)
        self.log_thread.start()

    def create_widgets(self):
        logging.info("Создание элементов интерфейса.")
        self.lots_button = ttk.Button(self, text="View Lots", width=20, style='Custom.TButton')
        self.lots_button.pack(pady=10)

        self.user_id_frame = ttk.Frame(self)
        self.user_id_frame.pack(pady=10)

        self.user_id_label = ttk.Label(self.user_id_frame, text="Enter User ID", style='Custom.TLabel')
        self.user_id_label.pack(expand=True)

        self.user_id_entry = ttk.Entry(self.user_id_frame, width=20, style="Custom.TEntry")
        self.user_id_entry.pack(pady=10)

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

        self.refresh_connect = ttk.Button(self, text="Refresh", style="Custom.TButton", command=self.bot.refresh_connect)
        self.refresh_connect.pack(pady=10)

        self.monitor_button = ttk.Button(self, text="Monitor Item", command=self.start_monitoring, width=20,
                                         style="Custom.TButton")
        self.monitor_button.pack(pady=10)

        self.stop_button = ttk.Button(self, text="Stop", command=self.stop_monitoring, width=20, style="Custom.TButton")
        self.stop_button.pack(pady=10)

        # Кнопка для открытия настроек
        self.settings_button = ttk.Button(self, text="Settings", command=self.open_settings, width=20, style="Custom.TButton")
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
                    column = index % 3
                    item_id = item["id"]
                    title = item["title"]
                    ttk.Button(self.items_frame, text=title,
                               command=lambda args=(item_id,title): self.id_current_item(*args)).grid(row=row, column=column)
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

    def start_monitoring(self):
        logging.info("Попытка запуска мониторинга.")
        user_id = self.user_id_entry.get()
        if not user_id.isdigit():
            messagebox.showerror("Error", "User ID should be a number.")
            logging.warning("Введен некорректный User ID.")
            return
        max_price = self.price_entry.get()
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
        if int(delay) <= 10 or int(delay) > 120:
            messagebox.showerror("Error", "Delay should be between 10 and 120.")
            logging.warning("Введена задержка вне допустимого диапазона.")
            return

        self.item_id = self._id_current_item
        self.name = self._name_current_item
        self.max_price = int(max_price)
        self.user_id = int(user_id)
        self.delay = int(delay)
        logging.info(f"Запуск мониторинга для Item ID: {self.item_id}, User ID: {self.user_id}, "
                     f"Max Price: {self.max_price}, Delay: {self.delay}.")
        self.bot.send_start_monitoring(item_id=self.item_id, max_price=self.max_price, delay=self.delay, user_id=self.user_id, name=self.name)

    def stop_monitoring(self):
        if self._id_current_item:
            logging.info(f"Попытка остановить мониторинг для Item ID: {self.item_id}.")
            self.bot.send_stop_monitoring(item_id=self.item_id, max_price=self.max_price, delay=self.delay, user_id=self.user_id)
        else:
            messagebox.showerror("Error", "Please select an item ID.")
    def open_settings(self):
        logging.info("Открытие окна настроек.")
        settings_window = Toplevel(self)
        settings_window.title("Settings")
        settings_window.geometry("300x200")

        self.ip_label = ttk.Label(settings_window, text="Server IP Address")
        self.ip_label.pack(pady=10)

        self.ip_entry = ttk.Entry(settings_window, width=30)
        self.ip_entry.insert(0, '92.51.38.164')  # Значение по умолчанию
        self.ip_entry.pack(pady=10)

        save_button = ttk.Button(settings_window, text="Save", command=self.save_settings)
        save_button.pack(pady=10)

    def save_settings(self):
        ip = self.ip_entry.get()
        if ip == self.bot.server_ip:
            messagebox.showerror("Error", "Server IP don't changed")
            return
        logging.info(f"Настройки сохранены, IP адрес сервера: {ip}")
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

class Client:
    def __init__(self):
        logging.info("Инициализация клиента.")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_ip = 'localhost'
        self.server_port = 8080
        self.running = False
        self.queue = queue.Queue()

        self.connect_to_server()

    def connect_to_server(self):
        try:
            self.sock.connect((self.server_ip, self.server_port))
            logging.info(f"Подключение к серверу {self.server_ip}:{self.server_port} установлено.")
            self.running = True

            # Запуск потока для прослушивания сервера
            self.listen_thread = threading.Thread(target=self.listen_to_server, daemon=True)
            self.listen_thread.start()
        except ConnectionRefusedError:
            logging.error(f"Не удалось подключиться к серверу {self.server_ip}:{self.server_port}.")
            messagebox.showerror("Error",f"Failed to connect to server {self.server_ip}:{self.server_port}.")

    def update_server_ip(self, ip):
        self.server_ip = ip
        self.connect_to_server()

    def listen_to_server(self):
        try:
            while self.running:
                data = self.sock.recv(4096)
                if data:
                    logging.info(f"Сообщение от сервера: {data.decode('utf-8')}")
                else:
                    logging.warning("Соединение с сервером закрыто.")
                    self.stop()
                    break
        except Exception as e:
            logging.error(f"Ошибка при получении данных от сервера: {e}")
            self.stop()

    def send_start_monitoring(self, item_id, user_id, max_price, delay, name):
        template = f"start monitoring item_id={item_id} user_id={user_id} max_price={max_price} delay={delay} name={name}"
        self.sock.send(template.encode())
        logging.info(f"Отправлено сообщение на сервер: {template}")

    def send_stop_monitoring(self, item_id):
        template = f"stop monitoring item_id={item_id}"
        self.sock.send(template.encode())
        logging.info(f"Отправлено сообщение на сервер: {template}")

    def refresh_connect(self):
        self.connect_to_server()
    def stop(self):
        logging.info("Остановка клиента.")
        self.running = False
        try:
            self.sock.close()
        except Exception as e:
            logging.error(f"Ошибка при закрытии сокета: {e}")

    def get_view(self):
        data = self.queue.get()
        return data

if __name__ == '__main__':
    logging.info("Запуск приложения.")
    app = VKBotGUI()
    app.mainloop()
    os.remove("vk_bot.log")
