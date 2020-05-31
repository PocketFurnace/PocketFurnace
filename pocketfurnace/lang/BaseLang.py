from pocketfurnace.lang.Messages import Messages


class BaseLang:

    @staticmethod
    def get(self, message, language):
        if language == "esp":
            if message in Messages.spanish_messages:
                return Messages.spanish_messages[message]
            else:
                return Messages.default_message
        else:
            # default language when not finding a valid language or if the language is english
            if message in Messages.english_messages:
                return Messages.english_messages[message]
            else:
                return Messages.default_message
