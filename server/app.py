from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db, Hero, Power, HeroPower
from flask_migrate import Migrate

app = Flask(__name__)

# Database configeration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
migrate = Migrate(app, db)
db.init_app(app)



# list of heroes
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

# details of a specific hero by ID
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

#  list of powers
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

# Power by ID
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

# specific superpower by ID
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

# Hero_Power 
@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()

    required_fields = ['strength', 'power_id', 'hero_id']
    if not all(field in data for field in required_fields):
        return jsonify({'errors': ['Validation errors: strength, power_id, and hero_id are required']}), 400

    hero = Hero.query.get(data['hero_id'])
    power = Power.query.get(data['power_id'])

    if not hero or not power:
        return jsonify({'errors': ['Validation errors: Hero or Power not found']}), 404

    valid_strengths = ['Strong', 'Weak', 'Average']
    if data['strength'] not in valid_strengths:
        return jsonify({'errors': ['Validation errors: Invalid strength value']}), 400

    # Posting Hero_Power association
    hero_power = HeroPower(hero=hero, power=power, strength=data['strength'])
    db.session.add(hero_power)
    db.session.commit()

    hero_data = {
        'id': hero.id,
        'name': hero.name,
        'super_name': hero.super_name,
        'powers': [{'id': p.id, 'name': p.name, 'description': p.description} for p in hero.powers]
    }
    return jsonify(hero_data), 201
   


if __name__ == '__main__':
    app.run(debug=True)
