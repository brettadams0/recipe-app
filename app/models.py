from . import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # MealPlan.recipes declares a relationship to Recipe, but nothing linked the
    # two tables, so SQLAlchemy raised NoForeignKeysError while configuring
    # mappers — which broke every query in the app, not just meal plans.
    # Nullable because a recipe can exist before it is added to a plan.
    meal_plan_id = db.Column(db.Integer, db.ForeignKey('meal_plan.id'), nullable=True)

class MealPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    recipes = db.relationship('Recipe', backref='meal_plan', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
