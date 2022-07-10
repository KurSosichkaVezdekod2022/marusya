import pickle
from flask import request, jsonify
from . import app
from .utils import cards
from . import utils
from random import choices, choice
import pprint

users = {}


@app.route("/", methods=["GET", "POST"])
def index():
    # with open("../data.pickle", 'rb') as f:
    #     users = pickle.load(f)
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
    if req["session"]["new"] or user_id not in list(users.keys()):
        users[user_id] = sum(choices(list(cards.values()), k=2))
        response["response"]["buttons"] = buttons
    elif req["request"].get("command", False):
        if req["request"]["command"] == "ещё":
            card = choice(list(cards.keys()))
            users[user_id] += cards[card]
            response["response"]["text"] = f"Вам выпала карта {card}"
            response["response"]["buttons"] = buttons
        elif req["request"]["command"] == "on_interrupt":
            ai_score = utils.funcs.get_ai_score()
            user_score = users[user_id]
            users.pop(user_id)
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
    response['response']['text'] += f'\nВаш счёт {users[user_id]}'
    # with open("../data.pickle", 'wb') as f:
    #     pickle.dump(users, f)

    pprint.pprint(response)
    return jsonify(response)



