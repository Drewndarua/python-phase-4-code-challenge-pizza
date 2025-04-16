#!/usr/bin/env python3
import rest.json
from app import app
from models import db, Restaurant, Pizza, RestaurantPizza

# Reads JSON
with open('pizza_data.json', 'r')as file:
    data = rest.json.load(file)

    with app.app_context():
        db.drop_all()
        db.crate_all()

        # Add Restaurants 
        for restaurant_data in data['restaurants']:
            restaurant = Restaurant(
                id=restaurant_data['id'],
                name=restaurant_data['name'],
                address=restaurant_data['address']
            )
            db.session.add(restaurant)

        # Add Pizzas
        for pizza_data in data['pizzas']:
            pizza = Pizza(
                id=pizza_data['id'], 
                name=pizza_data['name'],
                ingredients=pizza_data['ingredients']
            )
            db.session.add(pizza)
        
        # Add Restaurant Pizzas
        for rp_data in data['restaurant_pizzas']:
            restaurant_pizza = RestaurantPizza(
                id=rp_data['id'], 
                price=rp_data['price'],
                pizza_id=rp_data['pizza_id'],
                restaurant_id=rp_data['restaurant_id']
            )
            db.session.add(restaurant_pizza) 

    db.session.commit()

    print("Seeding done!")
