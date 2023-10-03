#!/usr/bin/env python3
import random
from models import Hero, HeroPower, Power, db
from app import app

print("🦸‍♀️ Seeding powers...")
power_list = [
    {
        "name": "super strength",
        "description": "gives the wielder super-human strengths",
    },
    {
        "name": "flight",
        "description": "gives the wielder the ability to fly through the skies at supersonic speed",
    },
    {
        "name": "super human senses",
        "description": "allows the wielder to use her senses at a super-human level",
    },
    {
        "name": "elasticity",
        "description": "can stretch the human body to extreme lengths",
    },
]

print("🦸‍♀️ Seeding heroes...")
hero_list = [
    {"name": "Kamala Khan", "super_name": "Ms. Marvel"},
    {"name": "Doreen Green", "super_name": "Squirrel Girl"},
    {"name": "Gwen Stacy", "super_name": "Spider-Gwen"},
    {"name": "Janet Van Dyne", "super_name": "The Wasp"},
    {"name": "Wanda Maximoff", "super_name": "Scarlet Witch"},
    {"name": "Carol Danvers", "super_name": "Captain Marvel"},
    {"name": "Jean Grey", "super_name": "Dark Phoenix"},
    {"name": "Ororo Munroe", "super_name": "Storm"},
    {"name": "Kitty Pryde", "super_name": "Shadowcat"},
    {"name": "Elektra Natchios", "super_name": "Elektra"},
]

print("🦸‍♀️ Adding powers to heroes...")

strengths = ["Strong", "Weak", "Average"]

with app.app_context():
    Hero.query.delete()
    Power.query.delete()
    HeroPower.query.delete()
    heroes = []
    for hero in hero_list:
        heroe = Hero(name=hero["name"], super_name=hero["super_name"])
        heroes.append(heroe)
    db.session.add_all(heroes)

    powers = []
    for power in power_list:
        pow = Power(name=power["name"], description=power["description"])
        powers.append(pow)
    db.session.add_all(powers)
    strs = []
    for strength in strengths:
        st = HeroPower(
            strength=strength,
            hero_id=random.randint(1, len(heroes)),
            power_id=random.randint(1, len(powers)),
        )
        strs.append(st)
    db.session.add_all(strs)

    db.session.commit()


print("🦸‍♀️ Done seeding!")