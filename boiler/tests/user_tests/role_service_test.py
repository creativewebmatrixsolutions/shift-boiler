from unittest import mock
from nose.plugins.attrib import attr
from boiler.testing.testcase import FlaskTestCase
from shiftschema.result import Result

from boiler.di import get_service
from boiler.user.role_service import RoleService
from boiler.user.models import Role
from boiler.user import events, exceptions as x


@attr('role', 'service')
class RoleServiceTests(FlaskTestCase):

    def setUp(self):
        super().setUp()
        self.create_db()

    # ------------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------------

    def test_instantiate(self):
        """ Creating role service """
        service = RoleService(db=mock.Mock())
        self.assertIsInstance(service, RoleService)

    def test_save_role_returns_errors_on_invalid(self):
        """ Saving invalid role returns error object """
        role = Role()
        role_service = get_service('user.role_service')
        res = role_service.save(role)
        self.assertIsInstance(res, Result)
        self.assertFalse(res)

    def test_save_role_possible(self):
        """ Saving valid role possible """
        role = Role(handle='admin')
        role_service = get_service('user.role_service')
        with events.events.disconnect_receivers():
            role = role_service.save(role)
            self.assertIsInstance(role, Role)
            self.assertIsNotNone(role.id)

    def test_save_role_emits_event(self):
        """ Saving role emits event """
        role = Role(handle='admin')
        role_service = get_service('user.role_service')
        with events.events.disconnect_receivers():
            spy = mock.Mock()
            events.role_saved_event.connect(spy, weak=False)
            role_service.save(role)
            spy.assert_called_with(role)

    def test_create_returns_errors_on_invalid(self):
        """ Creating role returns errors on invalid data """
        role_service = get_service('user.role_service')
        res = role_service.create('ad')
        self.assertIsInstance(res, Result)
        self.assertFalse(res)

    def test_create_role_possible(self):
        """ Can create role """
        role_service = get_service('user.role_service')
        with events.events.disconnect_receivers():
            role = role_service.create('admin')
            self.assertIsInstance(role, Role)
            self.assertIsNotNone(role.id)

    def test_create_role_emits_event(self):
        """ Creating a role emits event """
        role_service = get_service('user.role_service')
        with events.events.disconnect_receivers():
            spy = mock.Mock()
            events.role_created_event.connect(spy, weak=False)
            role = role_service.create('admin')
            spy.assert_called_with(role)

    def test_delete_role_possible(self):
        """ Deleting a role """
        role_service = get_service('user.role_service')
        with events.events.disconnect_receivers():
            role = role_service.create('admin')
            id = role.id
            self.assertIsNotNone(id)
            role_service.delete(role)
            self.assertIsNone(role_service.get(id))

    def test_delete_role_emits_event(self):
        """ Deleting a role emits event """
        role_service = get_service('user.role_service')
        with events.events.disconnect_receivers():
            role = role_service.create('admin')
            spy = mock.Mock()
            events.role_deleted_event.connect(spy, weak=False)
            role_service.delete(role)
            spy.assert_called_with(role)