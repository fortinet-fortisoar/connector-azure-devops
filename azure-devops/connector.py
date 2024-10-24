"""
Copyright start
MIT License
Copyright (c) 2024 Fortinet Inc
Copyright end
"""

from connectors.core.connector import Connector, get_logger, ConnectorError
from .operations import operations, _check_health
from connectors.core.utils import update_connnector_config


logger = get_logger('azure-devops')


class Azure(Connector):
    def execute(self, config, operation, params, *args, **kwargs):
        try:
            logger.info('In execute() Operation: {}'.format(operation))
            operation = operations.get(operation)
            return operation(config, params)
        except Exception as err:
            logger.error('An exception occurred {}'.format(err))
            raise ConnectorError('{}'.format(err))

    def check_health(self, config=None):
        try:
            config['connector_info'] = {"connector_name": self._info_json.get('name'),
                                        "connector_version": self._info_json.get('version')}
            return _check_health(config)
        except Exception as e:
            logger.exception("An exception occurred {}".format(e))
            raise ConnectorError(e)

    def on_update_config(self, old_config, new_config, active):
        connector_info = {"connector_name": self._info_json.get('name'),
                          "connector_version": self._info_json.get('version')}
        if new_config.get('auth_type') == 'On behalf of User - Delegate Permission':
            old_auth_code = old_config.get('code', '')
            new_auth_code = new_config.get('code', '')
            if old_auth_code != new_auth_code:
                new_config.pop('access_token', '')
            else:
                new_config['access_token'] = old_config.get('access_token')
                new_config['refresh_token'] = old_config.get('refresh_token')
                new_config['expiresOn'] = 0
        update_connnector_config(connector_info['connector_name'], connector_info['connector_version'], new_config,
                                 new_config['config_id'])
