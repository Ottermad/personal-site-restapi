"""User API tests."""
from app import db, create_app

from internal.test import APITestCase
from internal.test.factories.user import UserFactory
from internal.services import USER_SERVICE

import requests_mock
import json

user_factory = UserFactory()


class AuthAPITests(APITestCase):
    """User API tests."""

    def setUp(self):
        """Pass db and create_app to parent setUP method."""
        super(AuthAPITests, self).setUp(db, create_app)

    def test_jwt_create(self):
        """Test whether User can be created."""
        user = user_factory.new()
        with requests_mock.mock() as m:
            m.post(USER_SERVICE.host + '/authenticate', json={'pk': 18123})
            response = self.client.post(
                '/user/auth',
                data=json.dumps(user),
                headers={'Content-Type': 'application/json'}
            )

        self.assertEqual(response.status_code, 200)
