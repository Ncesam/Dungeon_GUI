import logging
import multiprocessing
import socket
import sqlite3
import time
from tkinter import messagebox


class Client:
    def __init__(self, host="localhost", port=5000):
        logging.info("Инициализация клиента.")
        self.server_ip = host
        self.server_port = port
        self.queue = multiprocessing.Queue()

    def connect_to_server(self):
        """
        Подключается к серверу и запускает процесс прослушивания.
        """
        try:
            self.sock = socket.create_connection((self.server_ip, self.server_port), timeout=2000)
            logging.info(f"Подключение к серверу {self.server_ip}:{self.server_port} установлено.")

            if hasattr(self, 'listen_process') and self.listen_process is not None:
                if self.listen_process.is_alive():
                    self.listen_process.terminate()
                    self.listen_process.join()

            # Запускаем процесс для прослушивания сервера
            self.listen_process = multiprocessing.Process(target=self.listen_to_server, daemon=True)
            self.listen_process.start()
        except ConnectionRefusedError:
            logging.error(f"Не удалось подключиться к серверу {self.server_ip}:{self.server_port}.")
            messagebox.showerror("Error", f"Failed to connect to server {self.server_ip}:{self.server_port}.")

    def refresh_connect(self):
        self.connect_to_server()

    def listen_to_server(self):
        """
        Процесс прослушивания сервера. Реагирует на паузы и получает сообщения.
        """
        try:
            while True:
                data = self.sock.recv(1024)
                if data:
                    try:
                        if data.decode("utf-8").startswith("SQLite"):
                            self.queue.put(data)
                            continue

                        logging.info(f"Сообщение от сервера: {data.decode('utf-8')}")
                        self.queue.put(data)
                    except UnicodeError:
                        self.queue.put(data)  # В случае ошибки кодирования
                else:
                    logging.warning("Соединение с сервером закрыто.")
                    self.queue.put(b'')  # Сигнализируем завершение передачи
                    self.stop()  # Останавливаем процесс
                    break
        except Exception as e:
            logging.error(f"Ошибка при получении данных от сервера: {e}")
            self.stop()

    def recv_db_file(self):
        """
        Получение файла от сервера и сохранение на диск.
        """
        with open('lot.db', 'wb') as file:
            logging.debug("Файл открыт")
            while True:
                chunk = self.queue.get()
                file.write(chunk)
                file.flush()
                if self.queue.empty():  # Если получен пустой чанк, значит данные закончились
                    logging.debug("Данные завершены, файл закрыт.")
                    break
                # Сброс буфера для записи на диск
            logging.debug("Файл сохранен успешно.")

    def send_start_monitoring(self, item_id, user_id, auth_key, max_price, delay, name, vk_token):
        """
        Отправляет команду на сервер для начала мониторинга.
        """
        template = f"start monitoring item_id={item_id} user_id={user_id} auth_key={auth_key} max_price={max_price} delay={delay} name={name} token={vk_token}"
        self.sock.send(template.encode())
        logging.info(f"Отправлено сообщение на сервер: {template}")

    def send_stop_monitoring(self, item_id, user_id):
        """
        Отправляет команду на сервер для остановки мониторинга.
        """
        template = f"stop monitoring item_id={item_id} user_id={user_id}"
        self.sock.send(template.encode())
        logging.info(f"Отправлено сообщение на сервер: {template}")

    def send_view_lots(self):
        """
        Отправляет запрос на просмотр лотов и обрабатывает полученный файл.
        """
        success = False
        while not success:
            template = "view lots"
            self.sock.send(template.encode())
            self.recv_db_file()  # Получаем файл
            # Читаем данные из базы
            conn = sqlite3.connect('lot.db')
            logging.info("Файл открывается")
            conn.isolation_level = None
            cursor = conn.cursor()
            try:
                cursor.execute('VACUUM;')
                list_lots = cursor.execute('SELECT * FROM lots ORDER BY time DESC;').fetchmany(10)
            except sqlite3.DatabaseError as e:
                continue
            conn.close()
            logging.info("Файл закрыт")
            message = "\n".join([f"{lot[1]} - {lot[2]} price: {lot[3]} in {lot[4]}" for lot in list_lots])
            messagebox.showinfo("Lots", message=message)
            success = True

    def update_server_ip(self, ip):
        self.server_ip = ip
        self.connect_to_server()

    def stop(self):
        """
        Останавливает клиента и завершает процессы.
        """
        logging.info("Остановка клиента.")
        try:
            self.sock.close()
        except Exception as e:
            logging.error(f"Ошибка при закрытии сокета: {e}")

        if hasattr(self, 'listen_process') and self.listen_process is not None:
            if self.listen_process.is_alive():
                logging.info("Завершение процесса прослушивания.")
                self.listen_process.terminate()
                self.listen_process.join()
            self.listen_process = None

    def retry_connect(self):
        """Попытка повторного подключения через 5 секунд."""
        logging.info("Попытка повторного подключения через 5 секунд.")
        time.sleep(5)
        self.connect_to_server()
