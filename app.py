#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        plants = Plant.query.all()
        plants_to_return = []

        for plant in plants:
            plant_dict = {
                "id": plant.id,
                "name": plant.name,
                "image": plant.image,
                "price": plant.price
            }

            plants_to_return.append(plant_dict)

        return jsonify(plants_to_return)
    
    def post(self):
        name= request.form.get("name")
        # print(name)
        image= request.form.get("image")
        price= request.form.get("price")

        plant=Plant(name=name, image=image, price=price)
        db.session.add(plant)
        db.session.commit()

        plants_dict={
                "id":plant.id,
                "name":plant.name,
                "image":plant.image,
                "price":plant.price

            }
        return make_response(jsonify(plants_dict), 201)


api.add_resource(Plants, '/plants')

class PlantByID(Resource):
    def get(self, plant_id):
        plant = Plant.query.filter_by(id=plant_id).first()

        if plant is None:
            return make_response(jsonify({"error": "Plant not found"}), 404)

        plant_dict = {
            "id": plant.id,
            "name": plant.name,
            "image": plant.image,
            "price": plant.price
        }

        return jsonify(plant_dict)


api.add_resource(PlantByID, '/plants/<int:plant_id>')

        

if __name__ == '__main__':
    app.run(port=5555, debug=True)