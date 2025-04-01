#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/restaurants/<int:id>", methods=["GET"])
def get_restaurants(id):
    restaurant = Restaurant.query.get(id)
    if restaurant:
        return make_response(restaurant.to_dict(rules=("restaurant_pizzas",)), 200)
    return make_response({"error": "Restaurant not found"}, 404)


@app.route("/restaurant/<int:id>", methods=["DELETE"])
def delete_restaurants(id):
    restaurant = Restaurant.query.get(id)
    if restaurant:
        db.session.delete(restaurant)
        db.session.commit()
        return make_response({}, 204)
    return make_response({"error": "Restaurant not found"}, 404)


@app.route("/restaurant_pizzas", methods=["POST"])
def create_restaurant_pizza():
    try:
        data = request.get_json()
        new_restaurant_pizza = RestaurantPizza(
            price=data["price"],
            restaurant_id=data["restaurant_id"],
            pizza_id=data["pizza_id"],
        )
        db.session.add(new_restaurant_pizza)
        db.session.commit()
        return make_response(new_restaurant_pizza.to_dict(), 201)
    
    except ValueError as e:
        return make_response({"errors": [str(e)]}, 400) 

    except Exception:
        return make_response({"errors": ["Invalid data"]}, 400)


if __name__ == "__main__":
    app.run(port=5555, debug=True)