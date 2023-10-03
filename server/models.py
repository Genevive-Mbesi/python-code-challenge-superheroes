from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Hero(db.Model):
    # Hero model fields
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    super_name = db.Column(db.String(255), nullable=False)
    powers = db.relationship('Power', secondary='hero_power', back_populates='heroes')

class Power(db.Model):
    # Power model fields
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    heroes = db.relationship('Hero', secondary='hero_power', back_populates='powers')

    @validates('description')
    def validate_description(self, key, description):
        if description != "" and len(description) < 20:
            raise ValueError("Description is required and must have a description of more than 20 characters in length")
        return description


class HeroPower(db.Model):
    # HeroPower model fields
    id = db.Column(db.Integer, primary_key=True)
    hero_id = db.Column(db.Integer, db.ForeignKey('hero.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('power.id'), nullable=False)
    strength = db.Column(db.String(255), nullable=False)
    
    @validates('strength')
    def validate_strength(self, key, strength):
        valid_strength = ['Strong', 'Weak', 'Average']
        if not strength in valid_strength:
            raise ValueError ('Strength must either be Strong or Weak or Average')
        return strength
