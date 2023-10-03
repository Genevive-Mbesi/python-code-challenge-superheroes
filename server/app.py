from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db, Hero, Power, HeroPower
from flask_migrate import Migrate

app = Flask(__name__)

# Database configeration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
migrate = Migrate(app, db)
db.init_app(app)

# Routes and API functionality

# Route to get a list of heroes
@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    hero_list = []
    for hero in heroes:
        hero_data = {
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name,
        }
        hero_list.append(hero_data)
    return jsonify(hero_list)

# Route to get details of a specific hero by ID
@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero_by_id(id):
    hero = Hero.query.get(id)
    if hero:
        hero_data = {
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name,
            'powers': [{'id': p.id, 'name': p.name, 'description': p.description} for p in hero.powers]
        }
        return jsonify(hero_data)
    else:
        return jsonify({'error': 'Hero not found'}), 404

# Route to get a list of superpowers
@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    power_list = []
    for power in powers:
        power_data = {
            'id': power.id,
            'name': power.name,
            'description': power.description,
        }
        power_list.append(power_data)
    return jsonify(power_list)

# Route to get details of a specific superpower by ID
@app.route('/powers/<int:id>', methods=['GET'])
def get_power_by_id(id):
    power = Power.query.get(id)
    if power:
        power_data = {
            'id': power.id,
            'name': power.name,
            'description': power.description,
        }
        return jsonify(power_data)
    else:
        return jsonify({'error': 'Power not found'}), 404

# Route to update the description of a specific superpower by ID
@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power_description(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({'error': 'Power not found'}), 404

    data = request.get_json()
    if 'description' in data:
        new_description = data['description']
        if len(new_description) >= 20:
            power.description = new_description
            db.session.commit()
            return jsonify({'id': power.id, 'name': power.name, 'description': power.description})
        else:
            return jsonify({'errors': ['Validation errors: Description must be at least 20 characters']}), 400
    else:
        return jsonify({'errors': ['Validation errors: Description is required']}), 400

if __name__ == '__main__':
    app.run(debug=True)
