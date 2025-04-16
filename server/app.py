#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask import Flask, jsonify, make_response, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///restaurant.json'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

@app.route("/restaurants", methods=["GET"])
def get_restaurants():
    restaurants = Restaurant.query.all()
    return jsonify([restaurant.to_dict(only=('id', 'name', 'address')) for restaurant in restaurants])

@app.route("/restaurant/<int:id>", methods=["GET"])
def get_restaurants(id):
    restaurant = Restaurant.query.get(id)
    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404
    return jsonify (restaurant.to_dict(only =('id', 'name', 'address', 'restaurant_pizzas')))

@app.route("/restaurants/<int:id>", methods=["DELETE"])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404
    db.session.delete(restaurant)
    db.session.commit()
    return make_response('', 204)

@app.route("/restaurant_pizzas", method=['POST'])
def create_restaurant_pizza():
    data = request.get_json()
    if not data or not all(key in data for key in ['price', 'pizza_id', 'restaurant_id']): 
        return jsonify({"errors": ["Missing required information"]}), 400
    
    try: 
        pizza = Pizza.query.get(data['pizza_id'])
        restaurant = Restaurant.query.get(data['restaurant_id'])
        if not pizza or not restaurant:
            return jsonify({"errors": ["Pizza or restaurant not found"]}), 400
        
        restaurant_pizza = RestaurantPizza(
            price=data['price'],
            pizza_id=data['pizza_id'],
            restaurant_id=data['restaurant_id']
        )
        db.session.add(restaurant)
        db.session.commit()

        return jsonify(restaurant_pizza.to_dict(only=( 
            'id', 'price', 'pizza_id', 'restaurant_id',
            'pizza.id', 'pizza.name', 'pizza.ingredients',
            'restaurant.id', 'restaurant.name', 'restaurant.address'
        ))), 201
    
    except (ValueError, IntegrityError) as e:
        db.sesssion.rollback()
        return jsonify({"errors": ["validate errors"]}), 400

if __name__ == "__main__":
    app.run(debug=True)