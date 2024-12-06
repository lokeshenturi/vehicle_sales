from utils.db import db


class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    year = db.Column(db.String(100), nullable=False)
    transmission = db.Column(db.String(100), nullable=False)