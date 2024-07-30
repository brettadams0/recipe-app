# Recipe Recommendation and Meal Planning Application

## Features

- User authentication and profile management.
- Browse and search for recipes by ingredients, cuisine, or dietary preferences.
- Generate meal plans for a week based on user preferences.
- Save favorite recipes and meal plans.
- Modern UI with responsive design.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/brettadams0/recipe-app.git
    cd recipe-app
    ```

2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

3. Set up the database:
    ```sh
    flask db init
    flask db migrate
    flask db upgrade
    ```

4. Run the application:
    ```sh
    flask run
    ```

## Usage

1. Register and log in to the application.
2. Browse and search for recipes.
3. Create meal plans and add recipes to them.
4. View and manage your meal plans.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.
