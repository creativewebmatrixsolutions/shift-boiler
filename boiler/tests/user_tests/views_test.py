from nose.plugins.attrib import attr
from kernel.testing.testcase import ClientTestCase

from datetime import datetime, timedelta
from flask import url_for, session

from kernel.user.services import user_service
from kernel.user import events
from kernel.user import views


@attr('user', 'views')
class UserViewsTest(ClientTestCase):
    """
    User views tests
    We are now going to test generic user views with integration testing.
    Since kernel views are not actually connected to routing we'll need
    to test those views through frontend.
    """

    def setUp(self):
        super().setUp()
        self.create_db()

    def create_user(self, password='123456'):
        """ A shortcut to quickly create and return a user """
        with events.events.disconnect_receivers():
            user = user_service.create(
                username='tester',
                email='test@test.com',
                password=password
            )

            user.confirm_email()
            user_service.save(user)

        return user


# ------------------------------------------------------------------------
# Login and logout
# ------------------------------------------------------------------------

    @attr('xxx')
    def test_login_possible(self):
        """ Can login with valid credentials """
        user = self.create_user()
        data = dict(email=user.email, password='123456')
        with events.events.disconnect_receivers():
            with self.app.test_request_context():
                res = self.post(url_for('user.login'), data=data)
                self.assertOkHtml(res)
                self.assertInResponse(res, views.Login.valid_message)
                # WE NEED TO MOUNT KERNEL USER VIEWS INTO TESTING APP