from flask import request, jsonify
from . import app
from .utils.Game import Board

users = dict()


@app.route("/", methods=["GET", "POST"])
def index():
    global users
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
        users[user_id] = Board()
        users[user_id].start_game()
    elif req["request"]["command"] == "налево":
        users[user_id].move(1)
    elif req["request"]["command"] == "направо":
        users[user_id].move(2)
    elif req["request"]["command"] == "вниз":
        users[user_id].move(3)
    elif req["request"]["command"] == "поворот":
        users[user_id].rotate_block()

    if users[user_id].game_running:
        response["response"]["buttons"] = buttons
        response["response"]["text"] = f"Ваш счёт: {users[user_id].score}\n\n{users[user_id].get_state()}"
    else:
        response["response"]["text"] = f"Игра окончена!\nВаш счёт: {users[user_id].score}"
        response["response"]["end_session"] = True
    print(len(response["response"]["text"]))

    return jsonify(response)



