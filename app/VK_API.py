import logging
import multiprocessing
import time
from tkinter import messagebox

import vk_api


class VKFishing:
    def __init__(self, token: str = None):
        if token is None:
            raise "Please enter a token"
        self.token = token
        self.session = vk_api.VkApi(token=token)
        self.vk = self.session.get_api()
        self.id_group = self.get_group()

    def start(self):
        self.process = multiprocessing.Process(target=run, args=(self.token, self.id_group), daemon=True)
        self.process.start()

    def stop(self):
        self.process.terminate()
        self.process.join()

    def get_group(self):
        list_conversation = self.vk.messages.getConversations(count=15)
        logging.info("Получены все чаты")
        for conversation in list_conversation['items']:
            if conversation['conversation']['peer']['type'] == 'group':
                group = self.vk.groups.getById(group_id=abs(conversation['conversation']['peer']['id']))
                if group[0]['name'] == "Подземелья колодца":
                    logging.info("Нашел группу")
                    return conversation['conversation']['peer']['id']


def run(token, id_group):
    if token is None:
        raise "Please enter a token"
    session = vk_api.VkApi(token=token)
    vk = session.get_api()
    while True:
        time.sleep(2)
        loop(vk, id_group)


def loop(vk, id_group):
    time.sleep(5)
    vk.messages.send(peer_id=id_group, random_id=0, message="Закинуть удочку")
    time.sleep(5)
    finded = False
    while not finded:
        messages = vk.messages.getHistory(count=3, offset=0,
                                              peer_id=id_group)
        time.sleep(10)
        for message in messages['items']:
            text = message['text']
            if text == "🚫Наживка в лодке закончилась!":
                messagebox.showerror("Error", "Наживок нету.")
                delete_message(vk, message_id=message['id'], peer_id=id_group)
                continue
            elif text == "Леска вытягивается очень тяжело...":
                messagebox.showinfo("Monster", "Пользователь наткнулся на монстра.")
                continue
            elif "Нaживки осталоcь" in text:
                bait = text.split(" ")[-1]
                print(bait)
                if bait == "0":
                    messagebox.showinfo("Baits", "Наживки кончились.")
                    delete_message(vk , message_id=message['id'], peer_id=id_group)
                    return
                logging.info(f"Left {bait} bait.")
                finded = True
                break
            else:
                continue


def delete_message(vk ,message_id, peer_id):
    vk.messages.delete(message_id=message_id, peer_id=peer_id)
    logging.debug('Message deleted')
