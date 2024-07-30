from app import create_app, db
from app.models import User, Recipe, MealPlan

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Recipe': Recipe, 'MealPlan': MealPlan}

if __name__ == '__main__':
    app.run(debug=True)
