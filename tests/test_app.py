"""End-to-end checks for the routes and models.

Every test here corresponds to a defect that made the app unusable: a missing
index blueprint, a base template copied from an unrelated project, a model
relationship with no foreign key, a missing user_loader, missing imports, and a
password hashing method Werkzeug 3 removed. They run against Flask's test
client with a throwaway SQLite database — no network, no fixtures to install.
"""

import os
import tempfile
import unittest

os.environ.setdefault("SECRET_KEY", "test-key")

from app import create_app, db  # noqa: E402
from app.models import MealPlan, Recipe, User  # noqa: E402


class AppTestCase(unittest.TestCase):
    def setUp(self):
        # ignore_cleanup_errors because Windows refuses to unlink the SQLite
        # file if any connection is still open when the directory is removed.
        self._dir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        db_path = os.path.join(self._dir.name, "test.db").replace(os.sep, "/")
        os.environ["DATABASE_URL"] = "sqlite:///" + db_path

        self.app = create_app()
        self.app.config.update(TESTING=True)
        self.client = self.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            # Release the file handle before the temp directory is removed.
            db.engine.dispose()
        self._dir.cleanup()

    def register(self, email="a@b.com", username="u", password="pw"):
        return self.client.post(
            "/register",
            data={"email": email, "username": username, "password": password},
        )

    def login(self, email="a@b.com", password="pw"):
        return self.client.post("/login", data={"email": email, "password": password})

    # -- routes ---------------------------------------------------------------

    def test_index_renders(self):
        # Nothing served "/" at all, while auth redirected to a 'main.index'
        # endpoint that did not exist.
        self.assertEqual(self.client.get("/").status_code, 200)

    def test_login_and_register_pages_render(self):
        # These extend base.html, which referenced endpoints from a different
        # project and raised BuildError on every render.
        self.assertEqual(self.client.get("/login").status_code, 200)
        self.assertEqual(self.client.get("/register").status_code, 200)

    def test_logout_redirects(self):
        self.register()
        self.login()
        self.assertEqual(self.client.get("/logout").status_code, 302)

    # -- auth -----------------------------------------------------------------

    def test_register_creates_user(self):
        self.assertIn(self.register().status_code, (200, 302))
        with self.app.app_context():
            self.assertIsNotNone(
                db.session.query(User).filter_by(email="a@b.com").first()
            )

    def test_password_is_hashed_with_a_salted_kdf(self):
        self.register()
        with self.app.app_context():
            user = db.session.query(User).filter_by(email="a@b.com").first()
            self.assertTrue(user.password.startswith("pbkdf2:sha256"))
            self.assertNotIn("pw", user.password)

    def test_login_redirects_home(self):
        self.register()
        response = self.login()
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.headers["Location"].endswith("/"))

    def test_bad_password_does_not_log_in(self):
        self.register()
        response = self.login(password="wrong")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.headers["Location"])

    def test_login_required_redirects_when_anonymous(self):
        self.assertEqual(self.client.get("/meal_plan").status_code, 302)

    def test_login_required_passes_once_authenticated(self):
        # Requires login_manager.user_loader, which was never defined.
        self.register()
        self.login()
        self.assertEqual(self.client.get("/meal_plan").status_code, 200)

    # -- models ---------------------------------------------------------------

    def test_meal_plan_recipe_relationship_resolves(self):
        # MealPlan.recipes had no foreign key linking the tables, so configuring
        # the mappers raised NoForeignKeysError and broke every query.
        with self.app.app_context():
            user = User(username="u2", email="c@d.com", password="x")
            db.session.add(user)
            db.session.commit()

            plan = MealPlan(name="Week 1", user_id=user.id)
            db.session.add(plan)
            db.session.commit()

            recipe = Recipe(
                name="Soup",
                ingredients="water",
                instructions="boil",
                user_id=user.id,
                meal_plan_id=plan.id,
            )
            db.session.add(recipe)
            db.session.commit()

            self.assertEqual([r.name for r in plan.recipes], ["Soup"])
            self.assertEqual(recipe.meal_plan.name, "Week 1")

    def test_create_meal_plan_route(self):
        # This view used redirect() and url_for() without importing either.
        self.register()
        self.login()
        response = self.client.post("/meal_plan", data={"name": "Week 1"})
        self.assertEqual(response.status_code, 302)


if __name__ == "__main__":
    unittest.main()
