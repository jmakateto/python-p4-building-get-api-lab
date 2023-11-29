#!/usr/bin/env python3

from flask import Flask, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route("/")
def index():
    return "<h1>Bakery GET API</h1>"


@app.route("/bakeries", methods=["GET"])
def get_bakeries():
    bakeries = Bakery.query.all()
    serialized_bakeries = [bakery.to_dict() for bakery in bakeries]
    return jsonify(serialized_bakeries)


@app.route("/bakeries/<int:id>", methods=["GET"])
def get_bakery(id):
    bakery = Bakery.query.get_or_404(id)
    return jsonify(bakery.to_dict())


@app.route("/baked_goods/by_price", methods=["GET"])
def get_baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    serialized_baked_goods = [bg.to_dict() for bg in baked_goods]
    return jsonify(serialized_baked_goods)


@app.route("/baked_goods/most_expensive", methods=["GET"])
def get_most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()
    return jsonify(most_expensive.to_dict())


if __name__ == "__main__":
    app.run(port=5555, debug=True)
