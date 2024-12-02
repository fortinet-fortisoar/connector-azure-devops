"""
Copyright start
MIT License
Copyright (c) 2024 Fortinet Inc
Copyright end
"""

import json
import requests
from .microsoft_api_auth import *
from connectors.core.connector import get_logger, ConnectorError
from .constants import *

logger = get_logger('azure-devops')


class AzureDevOps:
    def __init__(self, config):
        self.server_url = config.get('server_url').strip('/') + '/{0}'.format(config.get('organization'))
        if not (self.server_url.startswith('https://') or self.server_url.startswith('http://')):
            self.server_url = 'https://' + self.server_url
        self.username = ''
        self.auth_type = config.get('auth_type')
        self.headers = {
            'Content-Type': 'application/json'
        }
        self.auth = None
        if self.auth_type == 'Access Token':
            self.auth = (self.username, config.get('api_key'))
        else:
            ms_client = MicrosoftAuth(config)
            self.headers['Authorization'] = ms_client.get_validated_token(config, config.get('connector_info'))
        self.verify_ssl = config.get('verify_ssl')
        self.api_version = config.get('api_version') if config.get('api_version') not in [None, ''] else API_VERSION

    def make_request(self, endpoint, method='GET', data=None, params={}, files=None, is_url=False):
        try:
            url = endpoint if is_url else self.server_url + endpoint
            logger.info('Executing url {}'.format(url))
            params['api-version'] = self.api_version
            # CURL UTILS CODE
            try:
                from connectors.debug_utils.curl_script import make_curl
                make_curl(method, url, headers=self.headers, params=params, data=data, verify_ssl=self.verify_ssl)
            except Exception as err:
                logger.debug(f"Error in curl utils: {str(err)}")

            response = requests.request(method, url, auth=self.auth, params=params, files=files,
                                        data=data, headers=self.headers, verify=self.verify_ssl)
            if response.ok:
                logger.info('successfully get response for url {}'.format(url))
                if method.lower() == 'delete':
                    return response
                else:
                    if response.status_code == 304:
                        return None
                    elif response.status_code == 203:
                        raise ConnectorError("Invalid Access Token for the given organization.")
                    return response.json()
            else:
                try:
                    error_response = response.json()
                    if error_response.get('message'):
                        error_description = error_response['message']
                        raise ConnectorError({'error_description': error_description})
                    raise ConnectorError(error_response)
                except Exception as error:
                    logger.warning("error: {0}".format(error))
                    error_response = {
                        "status_code": response.status_code,
                        "error_message": response.text if response.text else response.reason
                    }
                    raise ConnectorError('Error occurred: {0}'.format(error_response))
        except requests.exceptions.SSLError:
            raise ConnectorError('SSL certificate validation failed')
        except requests.exceptions.ConnectTimeout:
            raise ConnectorError('The request timed out while trying to connect to the server')
        except requests.exceptions.ReadTimeout:
            raise ConnectorError('The server did not send any data in the allotted amount of time')
        except requests.exceptions.ConnectionError:
            raise ConnectorError('Invalid endpoint or credentials')
        except Exception as err:
            raise ConnectorError(str(err))
        raise ConnectorError(response.text)


def _check_health(config):
    try:
        if config.get('auth_type') == 'On behalf of User - Delegate Permission':
            check(config, config.get('connector_info'))
        list_projects(config, {"$top": 1})
        return True
    except Exception as err:
        logger.exception(str(err))
        raise ConnectorError(str(err))


def _build_payload(params):
    return {key: val for key, val in params.items() if val is not None and val != ''}


def handle_comma_separated_input(input_value):
    if input_value and isinstance(input_value, str):
        return [i.strip() for i in input_value.split(',') if i.strip()]
    if isinstance(input_value, (int, float)):
        return [input_value]
    return input_value


def list_pipelines(config, params):
    client = AzureDevOps(config)
    endpoint = '/{0}/_apis/pipelines'.format(params.pop('project', ''))
    field = params.pop('field', 'name') or 'name'
    order = params.pop('order', 'asc').lower() or 'asc'
    params['$orderBy'] = "{0} {1}".format(field, order)
    payload = _build_payload(params)
    return client.make_request(endpoint, params=payload)


def list_pipeline_runs(config, params):
    client = AzureDevOps(config)
    endpoint = '/{0}/_apis/pipelines/{1}/runs'.format(params.pop('project', ''), params.pop('pipelineId', ''))
    payload = _build_payload(params)
    return client.make_request(endpoint, params=payload)


def get_pipeline_run(config, params):
    client = AzureDevOps(config)
    endpoint = '/{0}/_apis/pipelines/{1}/runs/{2}'.format(params.get('project'), params.get('pipelineId'),
                                                          params.get('runId'))
    return client.make_request(endpoint)


# Need to check code with actual parameters
def run_pipeline(config, params):
    client = AzureDevOps(config)
    endpoint = '/{0}/_apis/pipelines/{1}/runs'.format(params.get('project'), params.get('pipelineId'))
    payload = {
        'stagesToSkip': handle_comma_separated_input(params.get('stagesToSkip')),
        'previewRun': params.get('previewRun'),
        'resources': params.get('resources'),
    }
    query_param = {
        'pipelineVersion': params.get('pipelineVersion', '')
    }
    payload = _build_payload(payload)
    return client.make_request(endpoint, method='POST', data=json.dumps(payload), params=query_param)


def list_projects(config, params):
    client = AzureDevOps(config)
    endpoint = "/_apis/projects"
    params['stateFilter'] = PROJECT_STATE_MAPPING.get(params.get('stateFilter', 'Well Formed'), params.get('stateFilter'))
    payload = _build_payload(params)
    return client.make_request(endpoint, params=payload)


def list_repositories(config, params):
    client = AzureDevOps(config)
    endpoint = "/{0}/_apis/git/repositories".format(params.pop('project', ''))
    payload = _build_payload(params)
    return client.make_request(endpoint, params=payload)


def list_branches(config, params):
    client = AzureDevOps(config)
    endpoint = "/{0}/_apis/git/repositories/{1}/refs".format(params.pop('project', ''), params.pop('repository', ''))
    payload = _build_payload(params)
    return client.make_request(endpoint, params=payload)


def list_commits(config, params):
    client = AzureDevOps(config)
    endpoint = "/{0}/_apis/git/repositories/{1}/commits".format(params.pop('project', ''),
                                                                params.pop('repositoryId', ''))
    params.pop('type', None)
    params['searchCriteria.ids'] = handle_comma_separated_input(params.get('searchCriteria.ids'))
    search_criteria = {'searchCriteria.{0}'.format(k): v for k, v in params.pop('searchCriteria', {}).items()
                       if v or isinstance(v, (int, bool))}
    params.update(search_criteria)
    query_params = _build_payload(params)
    return client.make_request(endpoint, params=query_params)


def get_commit(config, params):
    client = AzureDevOps(config)
    endpoint = "/{0}/_apis/git/repositories/{1}/commits/{2}" \
        .format(params.pop('project', ''), params.pop('repositoryId', ''), params.pop('commitId', ''))
    payload = _build_payload(params)
    return client.make_request(endpoint, params=payload)


def list_pull_requests(config, params):
    client = AzureDevOps(config)
    endpoint = "/{0}/_apis/git/repositories/{1}/pullrequests".format(
        params.pop('project', ''), params.pop('repositoryId', ''))
    params['searchCriteria.status'] = PROJECT_STATE_MAPPING.get(params.get('searchCriteria.status', 'Not Set'),
                                                                params.get('searchCriteria.status'))
    search_criteria = {'searchCriteria.{0}'.format(k): v for k, v in params.pop('searchCriteria', {}).items()}
    params.update(search_criteria)
    payload = _build_payload(params)
    return client.make_request(endpoint, params=payload)


def get_pull_requests_by_id(config, params):
    client = AzureDevOps(config)
    endpoint = "/{0}/_apis/git/pullrequests/{1}".format(
        params.pop('project', ''), params.pop('pullRequestId', ''))
    return client.make_request(endpoint)


def create_pull_request(config, params):
    client = AzureDevOps(config)
    additional_input = params.pop('additional_input', {})
    if additional_input and isinstance(additional_input, dict):
        params.update(additional_input)
    project = params.pop('project', '')
    repository = params.pop('repositoryId', '')
    endpoint = "/{0}/_apis/git/repositories/{1}/pullrequests".format(project, repository)
    query_param = {
        "supportsIterations": params.pop("supportsIterations", '')
    }
    query_param = _build_payload(query_param)
    reviewers = params.get('reviewers')
    reviewers = reviewers.split(',') if isinstance(reviewers, str) and reviewers else reviewers
    if reviewers:
        params['reviewers'] = [{"id": get_reviewer_id(config, reviewer.strip()), 'isRequired': True}
                               for reviewer in reviewers]
    params['targetRefName'] = get_ref_by_branch_name(config, project, repository, params['targetRefName'])
    params['sourceRefName'] = get_ref_by_branch_name(config, project, repository, params['sourceRefName'])
    payload = _build_payload(params)
    return client.make_request(endpoint, method='POST', params=query_param, data=json.dumps(payload))


def update_pull_request(config, params):
    client = AzureDevOps(config)
    if params.get('additional_input') and isinstance(params.get('additional_input'), dict):
        params.update(params.pop('additional_input', ''))
    project = params.pop('project', '')
    repository = params.pop('repositoryId', '')
    endpoint = "/{0}/_apis/git/repositories/{1}/pullrequests/{2}".format(project, repository,
                                                                         params.pop('pullRequestId', ''))
    params['status'] = PR_STATUS_MAPPING.get(params.get('status'))
    params['targetRefName'] = get_ref_by_branch_name(config, project, repository, params['targetRefName'])
    payload = _build_payload(params)
    return client.make_request(endpoint, method='PATCH', data=json.dumps(payload))


def list_pull_request_reviewers(config, params):
    client = AzureDevOps(config)
    endpoint = "/{0}/_apis/git/repositories/{1}/pullRequests/{2}/reviewers".format(
        params.pop('project', ''), params.pop('repositoryId', ''), params.pop('pullRequestId', ''))
    return client.make_request(endpoint)


def add_pull_request_reviewer(config, params):
    client = AzureDevOps(config)
    endpoint = "/{0}/_apis/git/repositories/{1}/pullRequests/{2}/reviewers".format(
        params.pop('project', ''), params.pop('repositoryId', ''), params.pop('pullRequestId', ''))
    payload = [{
        'id': get_reviewer_id(config, params.get('reviewerId')),
        'isRequired': params.get('isRequired', False)
    }]
    return client.make_request(endpoint, method='POST', data=json.dumps(payload))


def list_pull_request_commits(config, params):
    client = AzureDevOps(config)
    endpoint = "/{0}/_apis/git/repositories/{1}/pullRequests/{2}/commits?".format(params.pop('project', ''),
                                                                                  params.pop('repositoryId', ''),
                                                                                  params.pop('pullRequestId', ''))
    payload = _build_payload(params)
    return client.make_request(endpoint, params=payload)


def get_ref_by_branch_name(config, project, repository, branch_name):
    query_params = {
        "project": project,
        "repository": repository,
        "filterContains": branch_name,
        "limit": 1000
    }
    branches = list_branches(config, query_params).get('value')
    count = len(branches)
    if count == 1:
        return branches[0].get('name')
    for branch in branches:
        if branch.get('name', '') == 'refs/heads/{0}'.format(branch_name):
            return branch.get('name')
    return branch_name


def get_reviewer_id(config, query_string):
    try:
        client = AzureDevOps(config)
        endpoint = 'https://vssps.dev.azure.com/{0}/_apis/identities'.format(config.get('organization'))
        query_params = {
            'searchFilter': 'General',
            'filterValue': query_string
        }
        result = client.make_request(endpoint, params=query_params, is_url=True)
        reviewers = result.get('value')
        reviewer_id = None
        if result.get('count') == 0:
            logger.error("Reviewer {0} not found".format(query_string))
        elif result.get('count') == 1:
            reviewer_id = reviewers[0]['id']
        else:
            for reviewer in reviewers:
                if query_string == reviewers['providerDisplayName']:
                    reviewer_id = reviewer['id']
                    break
        if reviewer_id:
            return reviewer_id
        logger.error('Reviewer {0} not found, check if provided reviewer has appropriate permissions.'.format(query_string))
        return query_string
    except Exception as error:
        logger.exception('Error occurred while getting user ID. Error: {}'.format(error))
        return query_string


operations = {
    'list_pipelines': list_pipelines,
    'list_pipeline_runs': list_pipeline_runs,
    'get_pipeline_run': get_pipeline_run,
    'run_pipeline': run_pipeline,
    'list_projects': list_projects,
    'list_repositories': list_repositories,
    'list_branches': list_branches,
    'list_commits': list_commits,
    'get_commit': get_commit,
    'list_pull_requests': list_pull_requests,
    'get_pull_requests_by_id': get_pull_requests_by_id,
    'create_pull_request': create_pull_request,
    'update_pull_request': update_pull_request,
    'list_pull_request_reviewers': list_pull_request_reviewers,
    'add_pull_request_reviewer': add_pull_request_reviewer,
    'list_pull_request_commits': list_pull_request_commits,
    'check_health': _check_health
}
