from flask import request, jsonify
from . import app
from random import choice

users2 = dict()
objects = {"Яблоко": True, "Груша": True, "Банан": True, "Шоколад": True,
           "Сыр косичка": True, "Малина": True, "Чай": True, "Мороженое": True,
           "Пельмени": True, "Арбуз": True, "Дыня": True, "Абрикос": True,
           "Персик": True, "Вишня": True, "Сок": True, "Печенье": True,
           "Йогурт": True, "Мюсли": True, "Кофе": True, "Компот": True,
           "Стол": False, "Компьютер": False, "Наушники": False, "Телефон": False,
           "Скрепка": False, "Ручка": False, "Кружка": False, "Лампа": False,
           "Карандаш": False, "Гитара": False, "Толстовка": False, "Спутник": False,
           "Мотоцикл": False, "Велосипед": False, "Расческа": False, "Помада": False,
           "Тушь": False, "Книга": False, "Стул": False, "Мяч": False
           }


@app.route("/", methods=["GET", "POST"])
def index():
    global users2
    req = request.json
    response = {"response": {
        "tts": "",
        "text": "",
        "buttons": [],
        "end_session": False
    },
        "session": req["session"],
        "version": req["version"]}
    buttons = [{"title": "Съедобное"}, {"title": "Несъедобное"}]
    user_id = req["session"]["application"]["application_id"]
    if req["session"]["new"]:
        users2[user_id] = {"score": 0}
        users2[user_id]["last_word"] = choice(list(objects.keys()))
    elif req["request"]["command"] == "съедобное":
        if objects[users2[user_id]["last_word"]]:
            response["response"]["text"] = "Верно!\n"
            users2[user_id]["score"] += 1
        else:
            response["response"]["text"] = "Неверно :(\n"
            users2[user_id]["score"] = 0
        users2[user_id]["last_word"] = choice(list(objects.keys()))
    elif req["request"]["command"] == "несъедобное":
        if objects[users2[user_id]["last_word"]]:
            response["response"]["text"] = "Неверно :(\n"
            users2[user_id]["score"] = 0
        else:
            response["response"]["text"] = "Верно!\n"
            users2[user_id]["score"] += 1
        users2[user_id]["last_word"] = choice(list(objects.keys()))
    response["response"]["text"] += f'Ваш счёт: {users2[user_id]["score"]}\n' \
                                   f'Следующее слово: {users2[user_id]["last_word"]}'
    response["response"]["buttons"] = buttons
    return jsonify(response)



