import os
import datetime
import sys


class FileLogger:

    def __init__(self, dir_out, filename_without_ext, max_size_in_bytes):
        self.dir_out = dir_out
        self.filename_without_ext = filename_without_ext
        self.max_size_in_bytes = max_size_in_bytes

    def write_message(self, message):

        if not os.path.exists(self.dir_out):
            os.makedirs(self.dir_out)

        full_file_name = os.path.join(self.dir_out, self.filename_without_ext + ".txt")
        if not os.path.exists(full_file_name):
            open(full_file_name, 'a').close()
        if os.path.getsize(full_file_name) < self.max_size_in_bytes:
            with open(full_file_name, "a") as myfile:
                myfile.write("\n#######################################################\n")
                myfile.write(str(datetime.datetime.now()))
                myfile.write("\n")
                myfile.write(str(message))
                myfile.write("\n#######################################################\n")
        else:
            file_index = 1
            while True:
                full_file_name = os.path.join(self.dir_out, self.filename_without_ext, str(file_index) + ".txt")
                if os.path.getsize(full_file_name) < self.max_size_in_bytes:
                    with open(full_file_name, "a") as myfile:
                        myfile.write(str(message))
                else:
                    file_index += 1

    def make_message(self, parser_name, exception, url):
        message = "=================================================\n"
        type_, value_, traceback_ = sys.exc_info()
        message +=str(datetime.datetime.now())
        message +="\n"
        message += "Error in " + parser_name + "\n"
        message += "Error type:" + str(type_) + "\n"
        message += "Error value: " + str(value_) + "\n"
        message += "Error traceback: " + str(traceback_) + "\n"
        message += "error message: " + str(exception) + "\n"
        message += "url: " + url + "\n"
        message += "*************************************************" + "\n"
        return message


if __name__ == "__main__":
    logger = FileLogger("f:\\test\\", "test", 50000)
    logger.write_message("testing logger")
