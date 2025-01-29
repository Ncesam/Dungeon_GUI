import logging
import multiprocessing
import time
from tkinter import messagebox

import vk_api


class VKFishing:
    def __init__(self, token: str = None):
        if token is None:
            raise "Please enter a token"
        self.session = vk_api.VkApi(token=token)
        self.vk = self.session.get_api()
        self.id_group = self.get_group()

    def start(self):
        self.process = multiprocessing.Process(target=self.run)
        self.process.start()

    def run(self):
        while True:
            time.sleep(2)
            self.loop()

    def stop(self):
        self.process.terminate()
        self.process.join()

    def loop(self):
        self.vk.messages.send(peer_id=self.id_group, random_id=0, message="Закинуть удочку")
        time.sleep(5)
        message = self.vk.messages.getHistory(count=1, offset=0,
                                              peer_id=self.id_group)
        time.sleep(2)
        text = message['items'][0]['text']
        if text == "🚫Наживка в лодке закончилась!":
            messagebox.showerror("Error", "Наживок нету.")
            self.delete_message(message_id=message['id'], peer_id=self.id_group)
        elif text == "Леска вытягивается очень тяжело...":
            messagebox.showinfo("Monster", "Пользователь наткнулся на монстра.")
        elif "Нaживки осталоcь" in text:
            bait = text.split(" ")[2]
            if bait == "0":
                messagebox.showinfo("Baits", "Наживки кончились.")
                self.delete_message(message_id=message['id'], peer_id=self.id_group)
                return
            logging.info(f"Left {bait} bait.")

    def delete_message(self, message_id, peer_id):
        self.vk.messages.delete(message_id=message_id, peer_id=peer_id)
        logging.debug('Message deleted')

    def get_group(self):
        list_conversation = self.vk.messages.getConversations(count=15)
        logging.info("Получены все чаты")
        for conversation in list_conversation['items']:
            if conversation['conversation']['peer']['type'] == 'group':
                group = self.vk.groups.getById(group_id=abs(conversation['conversation']['peer']['id']))
                if group[0]['name'] == "Подземелья колодца":
                    logging.info("Нашел группу")
                    return conversation['conversation']['peer']['id']
