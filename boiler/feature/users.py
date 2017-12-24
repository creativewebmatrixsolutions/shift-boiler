from flask import session, g
from flask_login import current_user
from flask_principal import identity_loaded, UserNeed, RoleNeed
from flask_principal import Identity, AnonymousIdentity

from boiler.user.session_interface import BoilerSessionInterface
from boiler.user.services import login_manager, oauth, principal
from boiler.user.services import user_service
from boiler.user.util.oauth_providers import OauthProviders



def users_feature(app):
    """
    Add users feature
    Allows to register users and assign groups, instantiates flask login, flask principal
    and oauth integration
    """

    # use custom session interface
    app.session_interface = BoilerSessionInterface()

    # init user service
    user_service.init(app)

    # init login manager
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'
    login_manager.login_message = 'Please login'

    @login_manager.user_loader
    def load_user(id):
        return user_service.get(id)

    # init OAuth
    oauth.init_app(app)
    registry = OauthProviders(app)
    providers = registry.get_providers()
    with app.app_context():
        for provider in providers:
            if provider not in oauth.remote_apps:
                oauth.remote_app(provider, **providers[provider])
                registry.register_token_getter(provider)

    # init principal
    principal.init_app(app)

    @principal.identity_loader
    def load_identity():
        if current_user.is_authenticated:
            return Identity(current_user.id)
        session.pop('identity.name', None)
        session.pop('identity.auth_type', None)
        return AnonymousIdentity()

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        identity.user = current_user
        if not current_user.is_authenticated:
            return

        identity.provides.add(UserNeed(current_user.id))
        for role in current_user.roles:
            identity.provides.add(RoleNeed(role.handle))





