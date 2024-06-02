import unittest
from flask import current_app
from project import create_app, db
from project.models import User
from werkzeug.security import check_password_hash


class TestWebApp(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['WTF_CSRF_ENABLED'] = False  # no CSRF during tests
        self.appctx = self.app.app_context()
        self.appctx.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.appctx.pop()
        self.app = None
        self.appctx = None
        self.client = None

    def test_app(self):
        assert self.app is not None
        assert current_app == self.app


    def test_no_access_to_edit(self):
        """
        Test case to verify that unauthorised users cannot edit photos.

        With non-logged in user:
        Steps:
        1. Attempt to edit a photo with no user logged in
        2. Assert that the request is redirected to the /login page

        With logged in user:
        Steps:
        1. Attempt to edit a photo which was not uploaded by the currently logged in user
        2. Assert that an error message is shown.

        With an admin user:
        Steps:
        1. Attempt to edit a photo which was not uploaded by the admin user
        2. Assert that the user is able to access the edit page.

        """
        # TODO: Check that non-logged-in user should be redirected to /login
        assert False

    def test_register_user(self):
        """
        Test case to verify a user can sign up and is logged in automattically

        Steps:
        1.  Sign up a new user with some test credentials
        2. Assert that the new user is now logged in and redirected to the main page
        """
        pass


    def test_hashed_passwords(self):
        response = self.client.post('/signup', data = {
            'user' : 'testing user',
            'password' : 'test123'
        }, follow_redirects = True)

        user = User.query.filter_by(username='testing user').first()
        assert user is not None
        assert check_password_hash(user.password, 'test123')


    def test_sql_injection(self):
        """
        Test case to verify that SQL injection attacks are prevented.

        Steps:
            Test against sign up
        1. Attempt to sign up a new user with a username containing SQL injection payloads.
        2. Assert that the user is not created and an error message is shown.
            Test against log in
        1. Attempt to log in with a username and password containing SQL injection payloads.
        2. Assert that the login fails and an error message is shown.
        """
        # TODO: Implement the test cases
        pass
    def test_unauthorised_like_photo(self):
        """
        Test case to ensure that unauthorised users cannot like a photo.

        Steps:
        1. Attempt to access the '/like/<photo_id>/' endpoint without being authenticated.
        2. Assert that the request is redirected to the login page.
        """
        # TODO: Implement the test case
        pass
    def test_prevent_indexing_private(self):
        """
        Test case to ensure that private photos are not indexed by search engines.

        Steps:
        1. Create a private photo .
        2. Access the private photo witth the '/uploads/<private_photo_filename>' endpoint.
        3. Assert that the response headers include the 'X-Robots-Tag' header with the value 'noindex, nofollow'.
        """
        # TODO: Implement the test case
        pass
