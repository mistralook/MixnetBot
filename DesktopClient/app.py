import threading
import time

import py_cui

from Domain import send, get_updates, get_messages_by_pub_k
from Keys import generate_and_save_keys


class MixerMessenger:
    def __init__(self, master: py_cui.PyCUI):
        self.master = master
        self.chats_scroll_cell = self.master.add_scroll_menu('Chats', 0, 0, row_span=5, column_span=1)
        self.chats_scroll_cell.add_text_color_rule("", py_cui.WHITE_ON_BLACK, 'startswith',
                                                   selected_color=py_cui.MAGENTA_ON_BLACK)
        self.chat_cell = self.master.add_scroll_menu("Messages", 0, 1, 5, 5)
        self.add_chat = self.master.add_button(" + Chat", 5, 0, command=self.show_add_pub_k_text_box)
        self.generate_keys_btn = self.master.add_button("Generate keys", 6, 0, command=self.show_name_text_box)
        # self.get_updates_btn = self.master.add_button("Get updates", 7, 0, command=self.get_updates)
        self.input = self.master.add_text_box("Your input", 5, 1, 1, 5)

        self.chats_scroll_cell.add_key_command(py_cui.keys.KEY_ENTER, self.show_chat)
        self.input.add_key_command(py_cui.keys.KEY_ENTER, self.send_message)
        self.start_background_updating()
        self.chats = []

    def show_chat(self):
        self.chat_cell.clear()
        cur_receiver = self.chats_scroll_cell.get()
        if not cur_receiver:
            self.master.show_warning_popup("Warning", "No chats are available. Add chat first.")
            return
        self.chat_cell.set_title(f"Chat with: {cur_receiver}")
        self.update_chat(cur_receiver)

    def update_chat(self, sender_pub_k):
        self.chat_cell.clear()
        for m in get_messages_by_pub_k(sender_pub_k):
            self.chat_cell.add_item(m)

    def send_message(self):
        message = self.input.get()
        cur_receiver = self.chats_scroll_cell.get()
        if not cur_receiver:
            self.master.show_warning_popup("Warning", "Select receiver from 'Chats' menu")
            return
        send(recv_pub_k=cur_receiver, message=message)
        self.chat_cell.add_item(message)
        self.input.clear()

    def register_and_generate_keys(self, nickname):
        try:
            generate_and_save_keys(nickname)
            self.master.show_message_popup("DONE", 'Keys generated')
        except FileExistsError:
            self.master.show_warning_popup("Warning", 'Keys are already generated')

    def show_name_text_box(self):
        self.master.show_text_box_popup('Please enter your name', self.register_and_generate_keys)

    def quit_cui(self, to_quit):
        # THis is the function given to the yes no popup. The to_quit parameter will be True if y is pressed, or False if n is pressed
        if to_quit:
            exit()
        else:
            self.master.show_message_popup('Cancelled', 'The quit operation was cancelled.')

    def add_chat_to_list(self, receiver_pub_k):
        self.chats.append(receiver_pub_k)
        self.chats_scroll_cell._view_items = self.chats
        # self.chats_scroll_cell.add_item(receiver_pub_k)

    def show_add_pub_k_text_box(self):
        # Here, reset title is a function that takes a string parameter, which will be the user entered string
        self.master.show_text_box_popup('Please enter receiver pub k', self.add_chat_to_list)

    def reset_title(self, new_title):
        self.master.set_title(new_title)

    def start_background_updating(self):
        # return
        operation_thread = threading.Thread(target=self.background_update, daemon=True)
        operation_thread.start()

    def add_new_chats_from_updates(self, updated_chats):
        self.chats = list(set(self.chats).union(updated_chats))
        self.chats_scroll_cell._view_items = self.chats

    def background_update(self):
        while True:
            updated_chats, _ = get_updates()
            self.add_new_chats_from_updates(updated_chats)
            cur_chat = self.chats_scroll_cell.get()
            if cur_chat in updated_chats:
                self.update_chat(cur_chat)

            time.sleep(1)


# Create the CUI, pass it to the wrapper object, and start it
root = py_cui.PyCUI(8, 6)
root.set_title('MixerNet')
# root.enable_logging(logging_level=logging.DEBUG)
s = MixerMessenger(root)
root.start()
