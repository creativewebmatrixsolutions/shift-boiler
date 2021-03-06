from shiftschema.validators import AbstractValidator
from shiftschema.result import Error
from boiler.di import get_service


class UniqueUserProperty(AbstractValidator):
    error = 'Set proper error message'
    property = None

    def validate(self, value, context=None):
        """ Perform validation """
        self_id = None
        if context:
            if isinstance(context, dict): self_id = context.get('id')
            else: self_id = getattr(context, 'id')

        params = dict()
        params[self.property] = value
        user_service = get_service('user.user_service')
        found = user_service.first(**params)
        if not found or (context and self_id == found.id):
            return Error()

        return Error(self.error)


class UniqueUsername(UniqueUserProperty):
    """ Validates that provided username is unique """
    error = 'Username already exists'
    property = 'username'


class UniqueEmail(UniqueUserProperty):
    """ Validates that provided email is unique """
    error = 'Email already in use'
    property = 'email'


class UniqueRoleHandle(AbstractValidator):
    """ Role handle must be unique """
    error = 'Role handle already in use'

    def validate(self, value, context=None):
        """ Perform validation """
        self_id = None
        if context:
            if isinstance(context, dict): self_id = context.get('id')
            else: self_id = getattr(context, 'id')

        found = get_service('user.role_service').first(handle=value)
        if not found or (context and self_id == found.id):
            return Error()

        return Error(self.error)





