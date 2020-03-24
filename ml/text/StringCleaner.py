
class StringCleaner:

    @staticmethod
    def clean(message):

        message = message.strip()

        while message.find("  ") != -1:
            message = message.replace("  ", " ")

        while message.find("\t\t") != -1:
            message = message.replace("\t\t", "\t")

        while message.find("\n\n") != -1:
            message = message.replace("\n\n", "\n")

        return message


if __name__ == "__main__":
    #cleaner = StringCleaner()
    print(StringCleaner.clean("    testing     logger    "))
