from flask import Flask
from flask import render_template
from os import listdir
from os.path import isfile, join
from db import DbManager
from pathlib import Path
from miscellanea import ConfigManager
from miscellanea import FileLogger, FakeTestLogger, BackupManager
import os.path

app = Flask(__name__)


@app.route('/')
def index():
    # Инициализация.
    main_dir = Path(__file__).parents[0]
    config_file = os.path.join(main_dir, "config.json")

    config_manager = ConfigManager.ConfigManager()
    config_manager.read_config(config_file)
    logger = FakeTestLogger.FakeTestLogger()

    db_manager = DbManager.DbManager(config_manager, logger)

    # Запрос к БД.
    reports = db_manager.get_reports()

    # Преобразование полученных данных в массив словарей.
    reports_dict = []
    for report in reports:
        reports_dict.append(
            {'name': report[1]},
            {'decription': report[2]},
            {'columns': report[3]},
            {'x_title': report[4]},
            {'y_title': report[5]},
            {'body': report[6]}
        )

    # Передача в шаблон и его вызов.
    return render_template("index.html", reports=reports)


if __name__ == '__main__':
    app.run()
