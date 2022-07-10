from flask import request, jsonify
from . import app
from .utils.Game import Game, State

users5 = dict()


@app.route("/", methods=["GET", "POST"])
def index():
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



