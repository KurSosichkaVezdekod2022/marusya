from flask import request, jsonify
from . import app
from .utils.Game3 import Board

users3 = dict()


@app.route("/", methods=["GET", "POST"])
def index():
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
        users3[user_id] = Board()
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



