from flask import Flask
from flask import render_template
from os import listdir
from os.path import isfile, join
from db import DbManager
from pathlib import Path
from miscellanea import ConfigManager
from miscellanea import FileLogger, FakeTestLogger, BackupManager
import os.path
from werkzeug.debug import DebuggedApplication
from flask import Flask
import json

app = Flask(__name__)
app.run(debug=True)


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
    reports_db = db_manager.get_reports()

    # Преобразование полученных данных в массив словарей.
    reports = []
    i = 0
    for report in reports_db:
        reports.append(list(report))
        reports[i][3] = json.loads(report[3])
        i = i + 1
        # reports_dict.append(
        #    {'name': reports[1]},
        #    {'decription': reports[2]},
        #    {'columns': reports[3]},
        #    {'x_title': reports[4]},
        #    {'y_title': reports[5]},
        #    {'body': reports[6]}
        # )

    # Передача в шаблон и его вызов.
    # return render_template("index.html", reports=reports_dict)
    user = {'username': 'Miguel'}
    return render_template('index.html', title='Home', user=user, reports=reports)


if __name__ == '__main__':
    app.run(debug=True)
