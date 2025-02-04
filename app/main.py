from base64 import b64decode
import os

from Fortuna import random_int, random_float
from MonsterLab import Monster
from flask import Flask, render_template, request
from pandas import DataFrame

from app.data import Database
from app.graph import chart
from app.machine import Machine
from app.damage_parser import parse_damage
from MonsterLab.monster_data import Random


SPRINT = 3
APP = Flask(__name__)


@APP.route("/")
def home():
    return render_template(
        "home.html",
        sprint=f"Sprint {SPRINT}",
        monster=Monster().to_dict(),
        password=b64decode(b"VGFuZ2VyaW5lIERyZWFt"),
    )


@APP.route("/data", methods=["GET", "POST"])
def data():
    if SPRINT < 1:
        return render_template("data.html")
    
    db = Database()
    db.seed(1500)
    return render_template(
        "data.html",
        count=db.count(),
        table=db.html_table(),
    )

@APP.route("/reset", methods=["GET", "POST"])
def reset():
    db = Database()
    db.reset()
    return render_template(
        "data.html",
        count=db.count(),
        table=db.html_table(),    
        )

@APP.route("/view", methods=["GET", "POST"])
def view():
    if SPRINT < 2:
        return render_template("view.html")
    db = Database()
    options = ["Level", "Health", "Energy", "Sanity", "Low", "High", "Rarity"]
    x_axis = request.values.get("x_axis") or options[1]
    y_axis = request.values.get("y_axis") or options[2]
    target = request.values.get("target") or options[4]
    graph = chart(
        df=db.dataframe(),
        x=x_axis,
        y=y_axis,
        target=target
    ).to_json()
    return render_template(
        "view.html",
        options=options,
        x_axis=x_axis,
        y_axis=y_axis,
        target=target,
        count=db.count(),
        graph=graph,
    )


@APP.route("/model", methods=["GET", "POST"])
def model():
    if SPRINT < 3:
        return render_template("model.html")
    db = Database()
    options = ["Health", "Energy", "Sanity", "Low", "High", "Rarity"]
    filepath = os.path.join(os.path.dirname(__file__), "model.joblib")
    if not os.path.exists(filepath):
        df = db.dataframe()
        machine = Machine(df[options])
        machine.save(filepath)
    else:
        machine = Machine.open(filepath)

    stats = [[round(random_float(1, 250), 2) for _ in range(3)],
             [random_int(1, 84), random_int(232, 987)]]
    level = request.values.get("level", type=int) or random_int(1, 84)
    health = request.values.get("health", type=float) or stats[0].pop()
    energy = request.values.get("energy", type=float) or stats[0].pop()
    sanity = request.values.get("sanity", type=float) or stats[0].pop()
    low, high = (request.values.get("low", type=int), request.values.get("high", type=int)) or stats[1].pop()
    
    prediction, confidence = machine(DataFrame(
        [dict(zip(options, (health, energy, sanity, low, high)))]
    ))
    info = machine.info()
    return render_template(
        "model.html",
        info=info,
        level=level,
        health=health,
        energy=energy,
        sanity=sanity,
        low=low,
        high=high,
        prediction=prediction,
        confidence=f"{confidence:.2%}",
    )


if __name__ == '__main__':
    APP.run()
