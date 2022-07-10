from flask import request, jsonify
from . import app
from .utils import cards
from . import utils
from random import choices, choice

users1 = {}


@app.route("/", methods=["GET", "POST"])
def index():
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



