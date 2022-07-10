from flask import request, jsonify
from . import app
from .utils.Game4 import Board4
from .utils.Game3 import Board3
from .utils import cards, funcs
from .utils.Game import Game, State
from . import utils
from random import choices, choice

users1 = dict()
users2 = dict()
users3 = dict()
users4 = dict()
users5 = dict()

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


@app.route("/task10", methods=["GET", "POST"])
def task10():
    req = request.json
    response = {"response": {
        "tts": "",
        "text": "",
        "buttons": [],
        "end_session": False
    },
        "session": req["session"],
        "version": req["version"]}
    buttons = [{"title": "Ещё"}, {"title": "Хватит"}]
    user_id = req["session"]["session_id"]
    if req["session"]["new"] or user_id not in list(users1.keys()):
        users1[user_id] = sum(choices(list(cards.values()), k=2))
        response["response"]["buttons"] = buttons
    elif req["request"].get("command", False):
        if req["request"]["command"] == "ещё":
            card = choice(list(cards.keys()))
            users1[user_id] += cards[card]
            response["response"]["text"] = f"Вам выпала карта {card}"
            response["response"]["buttons"] = buttons
        elif req["request"]["command"] == "on_interrupt":
            ai_score = utils.funcs.get_ai_score()
            user_score = users1[user_id]
            users1.pop(user_id)
            response["response"]["end_session"] = True
            response["response"]["text"] = f"Счёт компьютера {ai_score}"
            if 21 >= ai_score > user_score:
                response["response"]["text"] += "\nВы проиграли"
            elif ai_score < user_score <= 21:
                response["response"]["text"] += "\nВы выиграли"
            else:
                response["response"]["text"] += "\nНичья"
            return jsonify(response)
    else:
        response["response"]["buttons"] = buttons
        response["response"]["text"] = "Я вас не понимаю"
    response['response']['text'] += f'\nВаш счёт {users1[user_id]}'

    return jsonify(response)


@app.route("/task20", methods=["GET", "POST"])
def task2():
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


@app.route("/task30", methods=["GET", "POST"])
def task3():
    global users3
    req = request.json
    response = {"response": {
        "tts": "",
        "text": "",
        "buttons": [],
        "end_session": False
    },
        "session": req["session"],
        "version": req["version"]}
    buttons = [{"title": "Налево"}, {"title": "Направо"}, {"title": "Вниз"}, {"title": "Поворот"}]
    user_id = req["session"]["application"]["application_id"]
    if req["session"]["new"]:
        users3[user_id] = Board3()
        users3[user_id].start_game()
    elif req["request"]["command"] == "налево":
        users3[user_id].move(1)
    elif req["request"]["command"] == "направо":
        users3[user_id].move(2)
    elif req["request"]["command"] == "вниз":
        users3[user_id].move(3)
    elif req["request"]["command"] == "поворот":
        users3[user_id].rotate_block()

    if users3[user_id].game_running:
        response["response"]["buttons"] = buttons
        response["response"]["text"] = f"Ваш счёт: {users3[user_id].score}\n\n{users3[user_id].get_state()}"
    else:
        response["response"]["text"] = f"Игра окончена!\nВаш счёт: {users3[user_id].score}"
        response["response"]["end_session"] = True
    print(len(response["response"]["text"]))

    return jsonify(response)


@app.route("/task40", methods=["GET", "POST"])
def task40():
    global users4
    req = request.json
    response = {"response": {
        "tts": "",
        "text": "",
        "buttons": [],
        "end_session": False
    },
        "session": req["session"],
        "version": req["version"]}
    buttons = [{"title": "Налево"}, {"title": "Направо"}, {"title": "Вниз"}, {"title": "Вверх"}]
    user_id = req["session"]["application"]["application_id"]
    if req["session"]["new"]:
        users4[user_id] = Board4()
        users4[user_id].start()
    elif req["request"]["command"] == "налево":
        users4[user_id].move('l')
    elif req["request"]["command"] == "направо":
        users4[user_id].move('r')
    elif req["request"]["command"] == "вниз":
        users4[user_id].move('d')
    elif req["request"]["command"] == "вверх":
        users4[user_id].move('u')

    if users4[user_id].game_running:
        response["response"]["buttons"] = buttons
        response["response"]["text"] = f"Ваш счёт: {users4[user_id].score}\n\n{users4[user_id].get_state()}"
    else:
        response["response"]["text"] = f"Игра окончена!\nВаш счёт: {users4[user_id].score}"
        response["response"]["end_session"] = True
    print(len(response["response"]["text"]))

    return jsonify(response)


@app.route("/task50", methods=["GET", "POST"])
def task5():
    global users5
    req = request.json
    response = {"response": {
        "tts": "",
        "text": "",
        "buttons": [],
        "end_session": False
    },
        "session": req["session"],
        "version": req["version"]}
    buttons = [{"title": "Влево"}, {"title": "Вправо"}, {"title": "Вниз"}, {"title": "Вверх"}]
    user_id = req["session"]["application"]["application_id"]
    if req["session"]["new"]:
        users5[user_id] = Game()
    elif req["request"]["command"] == "влево":
        users5[user_id].move('l')
    elif req["request"]["command"] == "вправо":
        users5[user_id].move('r')
    elif req["request"]["command"] == "вниз":
        users5[user_id].move('d')
    elif req["request"]["command"] == "вверх":
        users5[user_id].move('u')

    if users5[user_id].state == State.IN_PROGRESS:
        response["response"]["buttons"] = buttons
        response["response"]["text"] = f"Ваш счёт: {users5[user_id].score}\n\n{users5[user_id].get_state()}"
    else:
        if users5[user_id].state == State.FAIL:
            response["response"]["text"] = f"Игра окончена!\nВаш счёт: {users5[user_id].score}"
        else:
            response["response"]["text"] = f"Победа!\nВаш счёт: {users5[user_id].score}"

        response["response"]["end_session"] = True
    print(len(response["response"]["text"]))
    print(users5[user_id].board.array)
    print(response["response"]["text"])

    return jsonify(response)

