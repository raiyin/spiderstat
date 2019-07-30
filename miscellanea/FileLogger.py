import os
import datetime


class FileLogger:

    def __init__(self, dir_out, filename, max_size):
        self.dir_out = dir_out
        self.filename = filename
        self.max_size = max_size

    def write_message(self, message):
        full_fileName = os.path.join(self.dir_out, self.filename + ".txt")
        if not os.path.exists(full_fileName):
            with open(full_fileName, "w") as file:
                pass
        if os.path.getsize(full_fileName) < self.max_size:
            with open(full_fileName, "a") as myfile:
                myfile.write("\n#######################################################")
                myfile.write(str(datetime.datetime.now()))
                myfile.write("\n")
                myfile.write(message)
                myfile.write("\n#######################################################")
        else:
            file_index = 1
            while True:
                full_fileName = os.path.join(self.dir_out, self.filename, str(file_index) + ".txt")
                if os.path.getsize(full_fileName) < self.max_size:
                    with open(full_fileName, "a") as myfile:
                        myfile.write("\n#######################################################\n")
                        myfile.write(str(datetime.datetime.now()))
                        myfile.write("\n")
                        myfile.write(message)
                        myfile.write("\n#######################################################")
                else:
                    file_index += 1

    def make_message(self, parser_name, exception, url):
        pass


if __name__ == "__main__":
    logger = FileLogger("f:\\test\\", "test", 50000)
    logger.write_message("testing logger")
