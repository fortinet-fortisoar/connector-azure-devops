"""
Copyright start
MIT License
Copyright (c) 2024 Fortinet Inc
Copyright end
"""

from requests import request
from time import time, ctime
from datetime import datetime
from connectors.core.connector import get_logger, ConnectorError
from .constants import *
from connectors.core.utils import update_connnector_config

logger = get_logger('azure-devops')


class MicrosoftAuth:

    def __init__(self, config):
        self.client_id = config.get("client_id")
        self.client_secret = config.get("client_secret")
        self.verify_ssl = config.get('verify_ssl')
        tenant_id = 'organizations'
        self.auth_type = config.get("auth_type")
        self.auth_url = 'https://login.microsoftonline.com/{0}'.format(tenant_id)
        self.token_url = "https://login.microsoftonline.com/{0}/oauth2/v2.0/token".format(tenant_id)
        self.scope = "https://app.vssps.visualstudio.com/.default offline_access"
        self.refresh_token = ""
        self.code = config.get("code")
        self.redirect_url = config.get("redirect_url") if config.get("redirect_url") else DEFAULT_REDIRECT_URL

    def convert_ts_epoch(self, ts):
        datetime_object = datetime.strptime(ctime(ts), "%a %b %d %H:%M:%S %Y")
        return datetime_object.timestamp()

    def generate_token(self, refresh_token_flag):
        try:
            resp = self.acquire_token_on_behalf_of_user(refresh_token_flag)
            ts_now = time()
            resp['expiresOn'] = (ts_now + resp['expires_in']) if resp.get("expires_in") else None
            resp['access_token'] = resp.get("access_token")
            return resp
        except Exception as err:
            logger.error("{0}".format(err))
            raise ConnectorError("{0}".format(err))

    def get_validated_token(self, connector_config, connector_info):
        if CONFIG_SUPPORTS_TOKEN:
            ts_now = time()
            if not connector_config.get('access_token'):
                logger.error('Error occurred while connecting server: Unauthorized')
                raise ConnectorError('Error occurred while connecting server: Unauthorized')
            expires = connector_config['expiresOn']
            expires_ts = self.convert_ts_epoch(expires)
            if ts_now > float(expires_ts):
                REFRESH_TOKEN_FLAG = True
                logger.info("Token expired at {0}".format(expires))
                self.refresh_token = connector_config["refresh_token"]
                token_resp = self.generate_token(REFRESH_TOKEN_FLAG)
                connector_config['access_token'] = token_resp['access_token']
                connector_config['expiresOn'] = token_resp['expiresOn']
                connector_config['refresh_token'] = token_resp.get('refresh_token')
                update_connnector_config(connector_info['connector_name'], connector_info['connector_version'],
                                         connector_config,
                                         connector_config['config_id'])

                return "Bearer {0}".format(connector_config.get('access_token'))
            else:
                logger.info("Token is valid till {0}".format(expires))
                return "Bearer {0}".format(connector_config.get('access_token'))

    def acquire_token_on_behalf_of_user(self, refresh_token_flag):
        try:
            data = {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "redirect_uri": self.redirect_url,
                "scope": self.scope
            }

            if not refresh_token_flag:
                data["grant_type"] = AUTHORIZATION_CODE,
                data["code"] = self.code
            else:
                data['grant_type'] = REFRESH_TOKEN,
                data['refresh_token'] = self.refresh_token
            response = request("POST", self.token_url, data=data, verify=self.verify_ssl)
            if response.status_code in [200, 204, 201]:
                return response.json()

            else:
                if response.text != "":
                    error_msg = ''
                    err_resp = response.json()
                    if err_resp and 'error' in err_resp:
                        failure_msg = err_resp.get('error_description')
                        error_msg = 'Response {0}: {1} \n Error Message: {2}'.format(response.status_code,
                                                                                     response.reason,
                                                                                     failure_msg if failure_msg else '')
                    else:
                        err_resp = response.text
                else:
                    error_msg = '{0}:{1}'.format(response.status_code, response.reason)
                raise ConnectorError(error_msg)

        except Exception as err:
            logger.error("{0}".format(err))
            raise ConnectorError("{0}".format(err))


def check(config, connector_info):
    try:
        ms = MicrosoftAuth(config)
        if CONFIG_SUPPORTS_TOKEN:
            if 'access_token' not in config:
                token_resp = ms.generate_token(REFRESH_TOKEN_FLAG)
                config['access_token'] = token_resp.get('access_token')
                config['expiresOn'] = token_resp.get('expiresOn')
                config['refresh_token'] = token_resp.get('refresh_token')
                update_connnector_config(connector_info['connector_name'], connector_info['connector_version'], config,
                                         config['config_id'])
            else:
                ms.get_validated_token(config, connector_info)
            return True
    except Exception as err:
        raise ConnectorError(str(err))
