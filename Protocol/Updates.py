class UpdateType:
    up_to_date = "up_to_date"
    new_messages = "new_messages"
    all_messages = "all_messages"


class UpdField:
    messages = "messages"
    type = "type"


class Update:
    def __init__(self, upd_type: UpdateType, messages):
        self.type = upd_type
        self.messages = messages

    def to_dict(self):
        return {
            UpdField.messages: self.messages,
            UpdField.type: self.type
        }
