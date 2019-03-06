"""Entry point for the API that supports the Mycroft Marketplace."""
from flask import Flask

from selene.api import get_base_config, selene_api, SeleneResponse
from selene.api.endpoints import AccountEndpoint, AgreementsEndpoint
from selene.util.log import configure_logger
from .endpoints.account_preferences import AccountPreferencesEndpoint
from .endpoints.device import DeviceEndpoint
from .endpoints.device_count import DeviceCountEndpoint
from .endpoints.geography import GeographyEndpoint
from .endpoints.skills import SkillsEndpoint
from .endpoints.skill_settings import SkillSettingsEndpoint
from .endpoints.voice_endpoint import VoiceEndpoint
from .endpoints.wake_word_endpoint import WakeWordEndpoint

_log = configure_logger('account_api')


# Define the Flask application
acct = Flask(__name__)
acct.config.from_object(get_base_config())
acct.response_class = SeleneResponse
acct.register_blueprint(selene_api)

acct.add_url_rule(
    '/api/account',
    view_func=AccountEndpoint.as_view('account_api'),
    methods=['GET', 'POST']
)
acct.add_url_rule(
    '/api/agreement/<string:agreement_type>',
    view_func=AgreementsEndpoint.as_view('agreements_api'),
    methods=['GET']
)

skill_endpoint = SkillsEndpoint.as_view('skill_endpoint')
acct.add_url_rule(
    '/api/skills',
    view_func=skill_endpoint,
    methods=['GET']
)

setting_endpoint = SkillSettingsEndpoint.as_view('setting_endpoint')
acct.add_url_rule(
    '/api/skills/<string:skill_id>/settings',
    view_func=setting_endpoint,
    methods=['GET', 'PUT']
)

device_count_endpoint = DeviceCountEndpoint.as_view('device_count_endpoint')
acct.add_url_rule(
    '/api/device-count',
    view_func=device_count_endpoint,
    methods=['GET']
)

device_endpoint = DeviceEndpoint.as_view('device_endpoint')
acct.add_url_rule(
    '/api/devices',
    view_func=device_endpoint,
    methods=['GET']
)

preferences_endpoint = AccountPreferencesEndpoint.as_view(
    'preferences_endpoint'
)
acct.add_url_rule(
    '/api/preferences',
    view_func=preferences_endpoint,
    methods=['GET']
)

wake_word_endpoint = WakeWordEndpoint.as_view('wake_word_endpoint')
acct.add_url_rule(
    '/api/wake-words',
    view_func=wake_word_endpoint,
    methods=['GET']
)

voice_endpoint = VoiceEndpoint.as_view('voice_endpoint')
acct.add_url_rule(
    '/api/voices',
    view_func=voice_endpoint,
    methods=['GET']
)

geography_endpoint = GeographyEndpoint.as_view('geography_endpoint')
acct.add_url_rule(
    '/api/geographies',
    view_func=geography_endpoint,
    methods=['GET']
)