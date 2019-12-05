from datetime import datetime
from os import scandir, path, listdir
import shutil
import time
from distutils import dir_util


class BackupManager:
    # Класс создания бэкапов. В основном используется для бэкапа БД.

    def __init__(self, time_to_start, min_timeout, source_dir, dest_dir):

        #:param time_to_start: время дня, после которого начинать резервное копирование.
        #:param min_timeout: минимальный перерыв до следующего копирования секундах.
        #:param source_dir: директория для сохранения.
        #:param dest_dir: директория, в которую будет производиться резервное копирование.
        self.min_timeout = min_timeout
        self.time_to_start = time_to_start
        self.source_dir = source_dir
        self.dest_dir = dest_dir
        self.enabled = False

    def folder_size(self, path='.'):
        total = 0
        for entry in scandir(path):
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += self.folder_size(entry.path)
        return total

    def start_backup(self):

        self.enabled = True

        while True:
            # Смотрим текущее время дня. Если оно больше time_to_start, то начинаем копирование. Если нет, то спим 5
            # минут.
            if not self.enabled:
                return

            now = datetime.now()
            if now < self.time_to_start:
                time.sleep(5*60)
                continue
            else:
                break

        while True:
            # Смотрим вес копируемой директории и солько свободного места осталось. Если места хватает, то копируем.
            # Если не хватает, то смотрим самую старую директорию с префиксом равным названию сохраняемой директории
            # и удаляем ее. Идем на второй круг. Если все нормально, то копируем в директорию, которая называется как
            # директория источник плюс постфикс даты копирования.

            if not self.enabled:
                return

            source_dir_upper_name = path.basename(path.dirname(self.source_dir))
            source_dir_size = self.folder_size(self.source_dir)
            dest_free_space = shutil.disk_usage(self.dest_dir).free

            if source_dir_size > dest_free_space:
                dir_util.copy_tree(self.source_dir, self.dest_dir + source_dir_upper_name + "_" +
                                   datetime.now().strftime("%Y-%m-%d %H-%M-%S"))
                time.sleep(self.min_timeout)
            else:
                dir_list = [f for f in listdir(self.dest_dir) if path.isdir(path.join(self.dest_dir, f)) and
                            f.startswith(source_dir_upper_name)]
                dir_time_dict = {}
                for f in dir_list:
                    dir_time_dict[f] = datetime.strptime(f[len(source_dir_upper_name)+1:], "%Y-%m-%d %H-%M-%S")

                if len(dir_time_dict) == 0:
                    raise EnvironmentError("Not enough disc space")

                oldest_dir_time = sorted(dir_time_dict.values())[0]
                oldest_dir = ""
                for directory, dir_time in dir_time_dict.items():
                    if dir_time == oldest_dir_time:
                        oldest_dir = directory
                        break

                shutil.rmtree(path.join(self.dest_dir, oldest_dir))
                continue

    def stop_backup(self):
        self.enabled = False


if __name__ == "__main__":
    backup_manager = BackupManager(datetime(2019, 7, 30, 0, 0, 1), 24*60*60,
                                   "c:\\Users\\Lomonosov\\Desktop\\Vera phone\\WhatsApp Audio\\", "f:\\test\\")
    backup_manager.start_backup()
