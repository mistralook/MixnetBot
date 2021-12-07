import threading
import time
from threading import Thread
import py_cui

from Domain import send, save_updates, get_messages_by_pub_k
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
        self.get_updates_btn = self.master.add_button("Get updates", 7, 0, command=self.get_updates)
        self.input = self.master.add_text_box("Your input", 5, 1, 1, 5)

        self.chats_scroll_cell.add_key_command(py_cui.keys.KEY_ENTER, self.show_chat)
        self.input.add_key_command(py_cui.keys.KEY_ENTER, self.send_message)

        # buttons that will open each type of popup
        # self.show_message_popup = self.master.add_button('Show Message Popup', 0, 0, command=self.show_message)
        # self.show_yes_no_popup = self.master.add_button('Show Yes No Popup', 1, 0, command=self.show_yes_no)
        # self.show_loading_icon_popup = self.master.add_button('Show Loading Icon Popup', 2, 0,
        #                                                       command=self.show_loading_icon)
        # self.show_loading_bar_popup = self.master.add_button('Show Loading Bar Popup', 0, 1,
        #                                                      command=self.show_loading_bar)
        # self.show_text_box_popup = self.master.add_button('Show Text Box Popup', 1, 1, command=self.show_text_box)
        # self.show_menu_popup = self.master.add_button('Show Scroll Menu Popup', 2, 1, command=self.show_menu_popup_fun)

    # -------------------------------------------------------------------------------
    # First, the most simple popup, the message popup.
    # This will simply display a message, and is closed with enter, escape or space.
    # -------------------------------------------------------------------------------

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

    def get_updates(self):
        messages = save_updates()
        self.show_chat()

    def show_yes_no(self):
        """Displays a yes no popup asking if the user would like to quit
        """

        # For the yes/no popup, the 'command' parameter must take a function that requires a single boolean parameter
        self.master.show_yes_no_popup('Are you sure you want to quit?', self.quit_cui)

    def quit_cui(self, to_quit):
        # THis is the function given to the yes no popup. The to_quit parameter will be True if y is pressed, or False if n is pressed
        if to_quit:
            exit()
        else:
            self.master.show_message_popup('Cancelled', 'The quit operation was cancelled.')

    # -------------------------------------------------------------------------------
    # Next, the textbox popup. This works similar to the yes-no popup, but passes the
    # entered string into the callback function
    # -------------------------------------------------------------------------------
    def add_chat_to_list(self, receiver_pub_k):
        self.chats_scroll_cell.add_item(receiver_pub_k)

    def show_add_pub_k_text_box(self):
        # Here, reset title is a function that takes a string parameter, which will be the user entered string
        self.master.show_text_box_popup('Please enter receiver pub k', self.add_chat_to_list)

    def reset_title(self, new_title):
        self.master.set_title(new_title)

    # -------------------------------------------------------------------------------
    # The menu popup requires a list of strings, which will serve as menu items.
    # The callback function must take a single string parameter, same as the text box,
    # and this will simply be the selected menu item
    # -------------------------------------------------------------------------------

    def show_menu_popup_fun(self):
        # List of menu items
        menu_choices = ['RED', 'CYAN', 'MAGENTA']
        # Change button color function takes string, and depending on menu choices performs specific action
        self.master.show_menu_popup('Please select a new button color', menu_choices, self.change_button_color)

    def change_button_color(self, new_color):

        # Note how this menu callback function essentially "switches" on possible menu items
        color = py_cui.WHITE_ON_BLACK
        if new_color == "RED":
            color = py_cui.RED_ON_BLACK
        elif new_color == "CYAN":
            color = py_cui.CYAN_ON_BLACK
        elif new_color == "MAGENTA":
            color = py_cui.MAGENTA_ON_BLACK
        for key in self.master.get_widgets().keys():
            if isinstance(self.master.get_widgets()[key], py_cui.widgets.Button):
                self.master.get_widgets()[key].set_color(color)

    # -------------------------------------------------------------------------------
    # Finally, for loading popups, you are required to use some form of async/threading
    # Start the loading popup, and then the thread to perform the long operation in the same function.
    # Then, in your long operation function, at the end, close the loading popup. In the case of the loading bar
    # you can also increment the loading bar in the long operation.
    # -------------------------------------------------------------------------------

    def show_loading_icon(self):
        """Function that shows the usage for spwaning a loading icon popup
        """

        # The loading popup will remain onscreen until the stop loading function is called. Call this before a large operation, and call
        # stop after the operation is finished. Note that for these long operations, you must use a different thread
        # to not block the draw calls.
        self.master.show_loading_icon_popup('Please Wait', 'Loading')
        operation_thread = threading.Thread(target=self.long_operation)
        operation_thread.start()

    def show_loading_bar(self):
        """Function that shows the usage for spawning a loading bar popup
        """

        self.master.show_loading_bar_popup('Incrementing a counter...', 100)
        operation_thread = threading.Thread(target=self.long_operation)
        operation_thread.start()

    def long_operation(self):
        """A simple function that demonstrates a long callback operation performed while loading popup is open
        """

        counter = 0
        for _ in range(0, 100):
            time.sleep(0.1)
            counter = counter + 1
            self.master.status_bar.set_text(str(counter))
            # When using a bar indicator, we will increment the completed counter
            self.master.increment_loading_bar()
        self.master.stop_loading_popup()


def get_updates_background():
    while True:
        new_messages_senders = save_updates()

        time.sleep(5)


root = py_cui.PyCUI(8, 6)
root.set_title('MixerNet')
# root.enable_logging(logging_level=logging.DEBUG)
thread = Thread(target=get_updates_background)
thread.start()
s = MixerMessenger(root)
root.start()
