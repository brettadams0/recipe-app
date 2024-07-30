from flask import Blueprint, render_template, request
from flask_login import current_user, login_required
from .models import MealPlan, Recipe
from . import db

meal_plan = Blueprint('meal_plan', __name__)

@meal_plan.route('/meal_plan')
@login_required
def meal_plan_index():
    plans = MealPlan.query.filter_by(user_id=current_user.id).all()
    return render_template('meal_plan.html', meal_plans=plans)

@meal_plan.route('/meal_plan', methods=['POST'])
@login_required
def create_meal_plan():
    name = request.form.get('name')
    new_plan = MealPlan(name=name, user_id=current_user.id)
    db.session.add(new_plan)
    db.session.commit()
    return redirect(url_for('meal_plan.meal_plan_index'))

@meal_plan.route('/meal_plan/<int:plan_id>')
@login_required
def view_meal_plan(plan_id):
    plan = MealPlan.query.get_or_404(plan_id)
    return render_template('view_meal_plan.html', plan=plan)
