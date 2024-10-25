# Edit the config_and_params.json file and add the necessary parameter values.
"""
Copyright start
MIT License
Copyright (c) 2024 Fortinet Inc
Copyright end
"""

import os
import sys
import json
import pytest
import logging
import importlib
from connectors.core.connector import ConnectorError

with open('tests/config_and_params.json', 'r') as file:
    params = json.load(file)

current_directory = os.path.dirname(__file__)
parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
grandparent_directory = os.path.abspath(os.path.join(parent_directory, os.pardir))
sys.path.insert(0, str(grandparent_directory))

module_name = 'azure-devops_1_0_0.operations'
conn_operations_module = importlib.import_module(module_name)
operations = conn_operations_module.operations

with open('info.json', 'r') as file:
    info_json = json.load(file)

logger = logging.getLogger(__name__)


# To test with different configuration values, adjust the index in the list below.
@pytest.fixture(scope="module")
def valid_credentials():
    return params.get('config')[0]


@pytest.fixture(scope="module")
def valid_credentials_with_token(valid_credentials):
    config = valid_credentials
    operations['check_health'](config)
    return config


@pytest.mark.checkhealth
def test_check_health_success(valid_credentials):
    assert operations['check_health'](valid_credentials)


@pytest.mark.checkhealth
def test_check_health_invalid_server_url(valid_credentials):
    invalid_creds = valid_credentials.copy()
    invalid_creds['server_url'] = params.get('invalid_params')['text']
    with pytest.raises(ConnectorError):
        assert operations['check_health'](invalid_creds)


@pytest.mark.checkhealth
def test_check_health_invalid_organization(valid_credentials):
    invalid_creds = valid_credentials.copy()
    invalid_creds['organization'] = params.get('invalid_params')['text']
    with pytest.raises(ConnectorError):
        assert operations['check_health'](invalid_creds)


@pytest.mark.checkhealth
def test_check_health_invalid_api_version(valid_credentials):
    invalid_creds = valid_credentials.copy()
    invalid_creds['api_version'] = params.get('invalid_params')['text']
    with pytest.raises(ConnectorError):
        assert operations['check_health'](invalid_creds)


@pytest.mark.list_pipelines
@pytest.mark.parametrize("input_params", params['list_pipelines'])
def test_list_pipelines_success(valid_credentials_with_token, input_params):
    logger.info("params: {0}".format(input_params))
    assert operations['list_pipelines'](valid_credentials_with_token, input_params.copy())


# Ensure that the provided input_params yield the correct output schema, or adjust the index in the list below.
# conditional_output_schema not supported.
@pytest.mark.list_pipelines
@pytest.mark.schema_validation
def test_validate_list_pipelines_output_schema(valid_credentials_with_token):
    input_params = params.get('list_pipelines')[0]
    schema = {}
    for operation in info_json.get("operations"):
        if operation.get('operation') == 'list_pipelines':
            if operation.get('conditional_output_schema'):
                schema = {}
            else:
                schema = operation.get('output_schema')
            break
    logger.info("output_schema: {0}".format(schema))
    assert set(operations['list_pipelines'](valid_credentials_with_token, input_params.copy()).keys()) == set(
        schema.keys())


@pytest.mark.list_pipelines
def test_list_pipelines_invalid_project(valid_credentials_with_token):
    input_params = params.get('list_pipelines')[0].copy()
    input_params['project'] = params.get('invalid_params')['text']
    with pytest.raises(ConnectorError):
        assert operations['list_pipelines'](valid_credentials_with_token, input_params.copy())


@pytest.mark.list_pipeline_runs
@pytest.mark.parametrize("input_params", params['list_pipeline_runs'])
def test_list_pipeline_runs_success(valid_credentials_with_token, input_params):
    logger.info("params: {0}".format(input_params))
    result = operations['list_pipeline_runs'](valid_credentials_with_token, input_params.copy())
    assert result
    for pipeline_run in result.get('value'):
        params['get_pipeline_run'][0]['pipelineId'] = pipeline_run.get('pipeline').get('id')
        params['get_pipeline_run'][0]['runId'] = pipeline_run.get('id')


# Ensure that the provided input_params yield the correct output schema, or adjust the index in the list below.
# conditional_output_schema not supported.
@pytest.mark.list_pipeline_runs
@pytest.mark.schema_validation
def test_validate_list_pipeline_runs_output_schema(valid_credentials_with_token):
    input_params = params.get('list_pipeline_runs')[0]
    schema = {}
    for operation in info_json.get("operations"):
        if operation.get('operation') == 'list_pipeline_runs':
            if operation.get('conditional_output_schema'):
                schema = {}
            else:
                schema = operation.get('output_schema')
            break
    logger.info("output_schema: {0}".format(schema))
    assert set(operations['list_pipeline_runs'](valid_credentials_with_token, input_params.copy()).keys()) == set(
        schema.keys())


@pytest.mark.list_pipeline_runs
def test_list_pipeline_runs_invalid_project(valid_credentials_with_token):
    input_params = params.get('list_pipeline_runs')[0].copy()
    input_params['project'] = params.get('invalid_params')['text']
    with pytest.raises(ConnectorError):
        assert operations['list_pipeline_runs'](valid_credentials_with_token, input_params.copy())


@pytest.mark.list_pipeline_runs
def test_list_pipeline_runs_invalid_pipelineId(valid_credentials_with_token):
    input_params = params.get('list_pipeline_runs')[0].copy()
    input_params['pipelineId'] = params.get('invalid_params')['integer']
    with pytest.raises(ConnectorError):
        assert operations['list_pipeline_runs'](valid_credentials_with_token, input_params.copy())


@pytest.mark.get_pipeline_run
@pytest.mark.parametrize("input_params", params['get_pipeline_run'])
def test_get_pipeline_run_success(valid_credentials_with_token, input_params):
    logger.info("params: {0}".format(input_params))
    assert operations['get_pipeline_run'](valid_credentials_with_token, input_params.copy())


# Ensure that the provided input_params yield the correct output schema, or adjust the index in the list below.
# conditional_output_schema not supported.
@pytest.mark.get_pipeline_run
@pytest.mark.schema_validation
def test_validate_get_pipeline_run_output_schema(valid_credentials_with_token):
    input_params = params.get('get_pipeline_run')[0]
    schema = {}
    for operation in info_json.get("operations"):
        if operation.get('operation') == 'get_pipeline_run':
            if operation.get('conditional_output_schema'):
                schema = {}
            else:
                schema = operation.get('output_schema')
            break
    logger.info("output_schema: {0}".format(schema))
    assert set(operations['get_pipeline_run'](valid_credentials_with_token, input_params.copy()).keys()) == set(
        schema.keys())


@pytest.mark.get_pipeline_run
def test_get_pipeline_run_invalid_project(valid_credentials_with_token):
    input_params = params.get('get_pipeline_run')[0].copy()
    input_params['project'] = params.get('invalid_params')['text']
    with pytest.raises(ConnectorError):
        assert operations['get_pipeline_run'](valid_credentials_with_token, input_params.copy())


@pytest.mark.get_pipeline_run
def test_get_pipeline_run_invalid_pipelineId(valid_credentials_with_token):
    input_params = params.get('get_pipeline_run')[0].copy()
    input_params['pipelineId'] = params.get('invalid_params')['integer']
    with pytest.raises(ConnectorError):
        assert operations['get_pipeline_run'](valid_credentials_with_token, input_params.copy())


@pytest.mark.get_pipeline_run
def test_get_pipeline_run_invalid_runId(valid_credentials_with_token):
    input_params = params.get('get_pipeline_run')[0].copy()
    input_params['runId'] = params.get('invalid_params')['text']
    with pytest.raises(ConnectorError):
        assert operations['get_pipeline_run'](valid_credentials_with_token, input_params.copy())


@pytest.mark.list_projects
@pytest.mark.parametrize("input_params", params['list_projects'])
def test_list_projects_success(valid_credentials_with_token, input_params):
    logger.info("params: {0}".format(input_params))
    assert operations['list_projects'](valid_credentials_with_token, input_params.copy())


# Ensure that the provided input_params yield the correct output schema, or adjust the index in the list below.
# conditional_output_schema not supported.
@pytest.mark.list_projects
@pytest.mark.schema_validation
def test_validate_list_projects_output_schema(valid_credentials_with_token):
    input_params = params.get('list_projects')[0]
    schema = {}
    for operation in info_json.get("operations"):
        if operation.get('operation') == 'list_projects':
            if operation.get('conditional_output_schema'):
                schema = {}
            else:
                schema = operation.get('output_schema')
            break
    logger.info("output_schema: {0}".format(schema))
    assert set(operations['list_projects'](valid_credentials_with_token, input_params.copy()).keys()) == set(
        schema.keys())


@pytest.mark.list_repositories
@pytest.mark.parametrize("input_params", params['list_repositories'])
def test_list_repositories_success(valid_credentials_with_token, input_params):
    logger.info("params: {0}".format(input_params))
    assert operations['list_repositories'](valid_credentials_with_token, input_params.copy())


# Ensure that the provided input_params yield the correct output schema, or adjust the index in the list below.
# conditional_output_schema not supported.
@pytest.mark.list_repositories
@pytest.mark.schema_validation
def test_validate_list_repositories_output_schema(valid_credentials_with_token):
    input_params = params.get('list_repositories')[0]
    schema = {}
    for operation in info_json.get("operations"):
        if operation.get('operation') == 'list_repositories':
            if operation.get('conditional_output_schema'):
                schema = {}
            else:
                schema = operation.get('output_schema')
            break
    logger.info("output_schema: {0}".format(schema))
    assert set(operations['list_repositories'](valid_credentials_with_token, input_params.copy()).keys()) == set(
        schema.keys())


@pytest.mark.list_repositories
def test_list_repositories_invalid_project(valid_credentials_with_token):
    input_params = params.get('list_repositories')[0].copy()
    input_params['project'] = params.get('invalid_params')['text']
    with pytest.raises(ConnectorError):
        assert operations['list_repositories'](valid_credentials_with_token, input_params.copy())


@pytest.mark.list_branches
@pytest.mark.parametrize("input_params", params['list_branches'])
def test_list_branches_success(valid_credentials_with_token, input_params):
    logger.info("params: {0}".format(input_params))
    assert operations['list_branches'](valid_credentials_with_token, input_params.copy())


# Ensure that the provided input_params yield the correct output schema, or adjust the index in the list below.
# conditional_output_schema not supported.
@pytest.mark.list_branches
@pytest.mark.schema_validation
def test_validate_list_branches_output_schema(valid_credentials_with_token):
    input_params = params.get('list_branches')[0]
    schema = {}
    for operation in info_json.get("operations"):
        if operation.get('operation') == 'list_branches':
            if operation.get('conditional_output_schema'):
                schema = {}
            else:
                schema = operation.get('output_schema')
            break
    logger.info("output_schema: {0}".format(schema))
    assert set(operations['list_branches'](valid_credentials_with_token, input_params.copy()).keys()) == set(
        schema.keys())


@pytest.mark.list_branches
def test_list_branches_invalid_filterContains(valid_credentials_with_token):
    input_params = params.get('list_branches')[0].copy()
    input_params['filterContains'] = params.get('invalid_params')['text']
    with pytest.raises(ConnectorError):
        assert operations['list_branches'](valid_credentials_with_token, input_params.copy())


@pytest.mark.list_branches
def test_list_branches_invalid_filter(valid_credentials_with_token):
    input_params = params.get('list_branches')[0].copy()
    input_params['filter'] = params.get('invalid_params')['text']
    with pytest.raises(ConnectorError):
        assert operations['list_branches'](valid_credentials_with_token, input_params.copy())


@pytest.mark.list_branches
def test_list_branches_invalid_project(valid_credentials_with_token):
    input_params = params.get('list_branches')[0].copy()
    input_params['project'] = params.get('invalid_params')['text']
    with pytest.raises(ConnectorError):
        assert operations['list_branches'](valid_credentials_with_token, input_params.copy())


@pytest.mark.list_branches
def test_list_branches_invalid_repository(valid_credentials_with_token):
    input_params = params.get('list_branches')[0].copy()
    input_params['repository'] = params.get('invalid_params')['text']
    with pytest.raises(ConnectorError):
        assert operations['list_branches'](valid_credentials_with_token, input_params.copy())


@pytest.mark.get_commit
@pytest.mark.parametrize("input_params", params['get_commit'])
def test_get_commit_success(valid_credentials_with_token, input_params):
    logger.info("params: {0}".format(input_params))
    assert operations['get_commit'](valid_credentials_with_token, input_params.copy())


# Ensure that the provided input_params yield the correct output schema, or adjust the index in the list below.
# conditional_output_schema not supported.
@pytest.mark.get_commit
@pytest.mark.schema_validation
def test_validate_get_commit_output_schema(valid_credentials_with_token):
    input_params = params.get('get_commit')[0]
    schema = {}
    for operation in info_json.get("operations"):
        if operation.get('operation') == 'get_commit':
            if operation.get('conditional_output_schema'):
                schema = {}
            else:
                schema = operation.get('output_schema')
            break
    logger.info("output_schema: {0}".format(schema))
    assert set(operations['get_commit'](valid_credentials_with_token, input_params.copy()).keys()) == set(schema.keys())


@pytest.mark.get_commit
def test_get_commit_invalid_project(valid_credentials_with_token):
    input_params = params.get('get_commit')[0].copy()
    input_params['project'] = params.get('invalid_params')['text']
    with pytest.raises(ConnectorError):
        assert operations['get_commit'](valid_credentials_with_token, input_params.copy())


@pytest.mark.get_commit
def test_get_commit_invalid_repositoryId(valid_credentials_with_token):
    input_params = params.get('get_commit')[0].copy()
    input_params['repositoryId'] = params.get('invalid_params')['text']
    with pytest.raises(ConnectorError):
        assert operations['get_commit'](valid_credentials_with_token, input_params.copy())


@pytest.mark.get_commit
def test_get_commit_invalid_commitId(valid_credentials_with_token):
    input_params = params.get('get_commit')[0].copy()
    input_params['commitId'] = params.get('invalid_params')['text']
    with pytest.raises(ConnectorError):
        assert operations['get_commit'](valid_credentials_with_token, input_params.copy())


@pytest.mark.create_pull_request
@pytest.mark.parametrize("input_params", params['create_pull_request'])
@pytest.mark.schema_validation
def test_create_pull_request_success(valid_credentials_with_token, input_params):
    logger.info("params: {0}".format(input_params))
    response = operations['create_pull_request'](valid_credentials_with_token, input_params.copy())
    assert response
    pull_request_id = response.get('pullRequestId')
    if pull_request_id:
        params.get('update_pull_request')[0]['pullRequestId'] = pull_request_id
        params.get('get_pull_requests_by_id')[0]['pullRequestId'] = pull_request_id
        params.get('list_pull_request_reviewers')[0]['pullRequestId'] = pull_request_id
        params.get('add_pull_request_reviewer')[0]['pullRequestId'] = pull_request_id
        params.get('list_pull_request_commits')[0]['pullRequestId'] = pull_request_id
    for operation in info_json.get("operations"):
        if operation.get('operation') == 'create_pull_request':
            if operation.get('conditional_output_schema'):
                schema = {}
            else:
                schema = operation.get('output_schema')
            break
    assert set(response.keys()) == set(schema.keys())


@pytest.mark.create_pull_request
def test_create_pull_request_invalid_reviewers(valid_credentials_with_token):
    input_params = params.get('create_pull_request')[0].copy()
    input_params['reviewers'] = params.get('invalid_params')['text']
    with pytest.raises(ConnectorError):
        assert operations['create_pull_request'](valid_credentials_with_token, input_params.copy())


@pytest.mark.create_pull_request
def test_create_pull_request_invalid_title(valid_credentials_with_token):
    input_params = params.get('create_pull_request')[0].copy()
    input_params['title'] = params.get('invalid_params')['text']
    with pytest.raises(ConnectorError):
        assert operations['create_pull_request'](valid_credentials_with_token, input_params.copy())


@pytest.mark.create_pull_request
def test_create_pull_request_invalid_additional_input(valid_credentials_with_token):
    input_params = params.get('create_pull_request')[0].copy()
    input_params['additional_input'] = params.get('invalid_params')['json']
    with pytest.raises(ConnectorError):
        assert operations['create_pull_request'](valid_credentials_with_token, input_params.copy())


@pytest.mark.create_pull_request
def test_create_pull_request_invalid_project(valid_credentials_with_token):
    input_params = params.get('create_pull_request')[0].copy()
    input_params['project'] = params.get('invalid_params')['text']
    with pytest.raises(ConnectorError):
        assert operations['create_pull_request'](valid_credentials_with_token, input_params.copy())


@pytest.mark.create_pull_request
def test_create_pull_request_invalid_repositoryId(valid_credentials_with_token):
    input_params = params.get('create_pull_request')[0].copy()
    input_params['repositoryId'] = params.get('invalid_params')['text']
    with pytest.raises(ConnectorError):
        assert operations['create_pull_request'](valid_credentials_with_token, input_params.copy())


@pytest.mark.create_pull_request
def test_create_pull_request_invalid_sourceRefName(valid_credentials_with_token):
    input_params = params.get('create_pull_request')[0].copy()
    input_params['sourceRefName'] = params.get('invalid_params')['text']
    with pytest.raises(ConnectorError):
        assert operations['create_pull_request'](valid_credentials_with_token, input_params.copy())


@pytest.mark.create_pull_request
def test_create_pull_request_invalid_targetRefName(valid_credentials_with_token):
    input_params = params.get('create_pull_request')[0].copy()
    input_params['targetRefName'] = params.get('invalid_params')['text']
    with pytest.raises(ConnectorError):
        assert operations['create_pull_request'](valid_credentials_with_token, input_params.copy())


@pytest.mark.update_pull_request
@pytest.mark.parametrize("input_params", params['update_pull_request'])
def test_update_pull_request_success(valid_credentials_with_token, input_params):
    logger.info("params: {0}".format(input_params))
    assert operations['update_pull_request'](valid_credentials_with_token, input_params.copy())


# Ensure that the provided input_params yield the correct output schema, or adjust the index in the list below.
# conditional_output_schema not supported.
@pytest.mark.update_pull_request
@pytest.mark.schema_validation
def test_validate_update_pull_request_output_schema(valid_credentials_with_token):
    input_params = params.get('update_pull_request')[0]
    schema = {}
    for operation in info_json.get("operations"):
        if operation.get('operation') == 'update_pull_request':
            if operation.get('conditional_output_schema'):
                schema = {}
            else:
                schema = operation.get('output_schema')
            break
    logger.info("output_schema: {0}".format(schema))
    assert set(operations['update_pull_request'](valid_credentials_with_token, input_params.copy()).keys()) == set(
        schema.keys())


@pytest.mark.update_pull_request
def test_update_pull_request_invalid_pullRequestId(valid_credentials_with_token):
    input_params = params.get('update_pull_request')[0].copy()
    input_params['pullRequestId'] = params.get('invalid_params')['text']
    with pytest.raises(ConnectorError):
        assert operations['update_pull_request'](valid_credentials_with_token, input_params.copy())


@pytest.mark.update_pull_request
def test_update_pull_request_invalid_project(valid_credentials_with_token):
    input_params = params.get('update_pull_request')[0].copy()
    input_params['project'] = params.get('invalid_params')['text']
    with pytest.raises(ConnectorError):
        assert operations['update_pull_request'](valid_credentials_with_token, input_params.copy())


@pytest.mark.update_pull_request
def test_update_pull_request_invalid_repositoryId(valid_credentials_with_token):
    input_params = params.get('update_pull_request')[0].copy()
    input_params['repositoryId'] = params.get('invalid_params')['text']
    with pytest.raises(ConnectorError):
        assert operations['update_pull_request'](valid_credentials_with_token, input_params.copy())


@pytest.mark.update_pull_request
def test_update_pull_request_invalid_targetRefName(valid_credentials_with_token):
    input_params = params.get('update_pull_request')[0].copy()
    input_params['targetRefName'] = params.get('invalid_params')['text']
    with pytest.raises(ConnectorError):
        assert operations['update_pull_request'](valid_credentials_with_token, input_params.copy())


@pytest.mark.list_pull_requests
@pytest.mark.parametrize("input_params", params['list_pull_requests'])
def test_list_pull_requests_success(valid_credentials_with_token, input_params):
    logger.info("params: {0}".format(input_params))
    assert operations['list_pull_requests'](valid_credentials_with_token, input_params.copy())


# Ensure that the provided input_params yield the correct output schema, or adjust the index in the list below.
# conditional_output_schema not supported.
@pytest.mark.list_pull_requests
@pytest.mark.schema_validation
def test_validate_list_pull_requests_output_schema(valid_credentials_with_token):
    input_params = params.get('list_pull_requests')[0]
    schema = {}
    for operation in info_json.get("operations"):
        if operation.get('operation') == 'list_pull_requests':
            if operation.get('conditional_output_schema'):
                schema = {}
            else:
                schema = operation.get('output_schema')
            break
    logger.info("output_schema: {0}".format(schema))
    assert set(operations['list_pull_requests'](valid_credentials_with_token, input_params.copy()).keys()) == set(
        schema.keys())


@pytest.mark.list_pull_requests
def test_list_pull_requests_invalid_project(valid_credentials_with_token):
    input_params = params.get('list_pull_requests')[0].copy()
    input_params['project'] = params.get('invalid_params')['text']
    with pytest.raises(ConnectorError):
        assert operations['list_pull_requests'](valid_credentials_with_token, input_params.copy())


@pytest.mark.list_pull_requests
def test_list_pull_requests_invalid_repositoryId(valid_credentials_with_token):
    input_params = params.get('list_pull_requests')[0].copy()
    input_params['repositoryId'] = params.get('invalid_params')['text']
    with pytest.raises(ConnectorError):
        assert operations['list_pull_requests'](valid_credentials_with_token, input_params.copy())


@pytest.mark.get_pull_requests_by_id
@pytest.mark.parametrize("input_params", params['get_pull_requests_by_id'])
def test_get_pull_requests_by_id_success(valid_credentials_with_token, input_params):
    logger.info("params: {0}".format(input_params))
    assert operations['get_pull_requests_by_id'](valid_credentials_with_token, input_params.copy())


# Ensure that the provided input_params yield the correct output schema, or adjust the index in the list below.
# conditional_output_schema not supported.
@pytest.mark.get_pull_requests_by_id
@pytest.mark.schema_validation
def test_validate_get_pull_requests_by_id_output_schema(valid_credentials_with_token):
    input_params = params.get('get_pull_requests_by_id')[0]
    schema = {}
    for operation in info_json.get("operations"):
        if operation.get('operation') == 'get_pull_requests_by_id':
            if operation.get('conditional_output_schema'):
                schema = {}
            else:
                schema = operation.get('output_schema')
            break
    logger.info("output_schema: {0}".format(schema))
    assert set(operations['get_pull_requests_by_id'](valid_credentials_with_token, input_params.copy()).keys()) == set(
        schema.keys())


@pytest.mark.get_pull_requests_by_id
def test_get_pull_requests_by_id_invalid_project(valid_credentials_with_token):
    input_params = params.get('get_pull_requests_by_id')[0].copy()
    input_params['project'] = params.get('invalid_params')['text']
    with pytest.raises(ConnectorError):
        assert operations['get_pull_requests_by_id'](valid_credentials_with_token, input_params.copy())


@pytest.mark.get_pull_requests_by_id
def test_get_pull_requests_by_id_invalid_pullRequestId(valid_credentials_with_token):
    input_params = params.get('get_pull_requests_by_id')[0].copy()
    input_params['pullRequestId'] = params.get('invalid_params')['integer']
    with pytest.raises(ConnectorError):
        assert operations['get_pull_requests_by_id'](valid_credentials_with_token, input_params.copy())


@pytest.mark.list_pull_request_reviewers
@pytest.mark.parametrize("input_params", params['list_pull_request_reviewers'])
def test_list_pull_request_reviewers_success(valid_credentials_with_token, input_params):
    logger.info("params: {0}".format(input_params))
    assert operations['list_pull_request_reviewers'](valid_credentials_with_token, input_params.copy())


# Ensure that the provided input_params yield the correct output schema, or adjust the index in the list below.
# conditional_output_schema not supported.
@pytest.mark.list_pull_request_reviewers
@pytest.mark.schema_validation
def test_validate_list_pull_request_reviewers_output_schema(valid_credentials_with_token):
    input_params = params.get('list_pull_request_reviewers')[0]
    schema = {}
    for operation in info_json.get("operations"):
        if operation.get('operation') == 'list_pull_request_reviewers':
            if operation.get('conditional_output_schema'):
                schema = {}
            else:
                schema = operation.get('output_schema')
            break
    logger.info("output_schema: {0}".format(schema))
    assert set(
        operations['list_pull_request_reviewers'](valid_credentials_with_token, input_params.copy()).keys()) == set(
        schema.keys())


@pytest.mark.list_pull_request_reviewers
def test_list_pull_request_reviewers_invalid_project(valid_credentials_with_token):
    input_params = params.get('list_pull_request_reviewers')[0].copy()
    input_params['project'] = params.get('invalid_params')['text']
    with pytest.raises(ConnectorError):
        assert operations['list_pull_request_reviewers'](valid_credentials_with_token, input_params.copy())


@pytest.mark.list_pull_request_reviewers
def test_list_pull_request_reviewers_invalid_repositoryId(valid_credentials_with_token):
    input_params = params.get('list_pull_request_reviewers')[0].copy()
    input_params['repositoryId'] = params.get('invalid_params')['text']
    with pytest.raises(ConnectorError):
        assert operations['list_pull_request_reviewers'](valid_credentials_with_token, input_params.copy())


@pytest.mark.list_pull_request_reviewers
def test_list_pull_request_reviewers_invalid_pullRequestId(valid_credentials_with_token):
    input_params = params.get('list_pull_request_reviewers')[0].copy()
    input_params['pullRequestId'] = params.get('invalid_params')['text']
    with pytest.raises(ConnectorError):
        assert operations['list_pull_request_reviewers'](valid_credentials_with_token, input_params.copy())


@pytest.mark.add_pull_request_reviewer
@pytest.mark.parametrize("input_params", params['add_pull_request_reviewer'])
def test_add_pull_request_reviewer_success(valid_credentials_with_token, input_params):
    logger.info("params: {0}".format(input_params))
    assert operations['add_pull_request_reviewer'](valid_credentials_with_token, input_params.copy())


# Ensure that the provided input_params yield the correct output schema, or adjust the index in the list below.
# conditional_output_schema not supported.
@pytest.mark.add_pull_request_reviewer
@pytest.mark.schema_validation
def test_validate_add_pull_request_reviewer_output_schema(valid_credentials_with_token):
    input_params = params.get('add_pull_request_reviewer')[0]
    schema = {}
    for operation in info_json.get("operations"):
        if operation.get('operation') == 'add_pull_request_reviewer':
            if operation.get('conditional_output_schema'):
                schema = {}
            else:
                schema = operation.get('output_schema')
            break
    logger.info("output_schema: {0}".format(schema))
    assert set(
        operations['add_pull_request_reviewer'](valid_credentials_with_token, input_params.copy()).keys()) == set(
        schema.keys())


@pytest.mark.add_pull_request_reviewer
def test_add_pull_request_reviewer_invalid_reviewerId(valid_credentials_with_token):
    input_params = params.get('add_pull_request_reviewer')[0].copy()
    input_params['reviewerId'] = params.get('invalid_params')['text']
    with pytest.raises(ConnectorError):
        assert operations['add_pull_request_reviewer'](valid_credentials_with_token, input_params.copy())


@pytest.mark.add_pull_request_reviewer
def test_add_pull_request_reviewer_invalid_project(valid_credentials_with_token):
    input_params = params.get('add_pull_request_reviewer')[0].copy()
    input_params['project'] = params.get('invalid_params')['text']
    with pytest.raises(ConnectorError):
        assert operations['add_pull_request_reviewer'](valid_credentials_with_token, input_params.copy())


@pytest.mark.add_pull_request_reviewer
def test_add_pull_request_reviewer_invalid_repositoryId(valid_credentials_with_token):
    input_params = params.get('add_pull_request_reviewer')[0].copy()
    input_params['repositoryId'] = params.get('invalid_params')['text']
    with pytest.raises(ConnectorError):
        assert operations['add_pull_request_reviewer'](valid_credentials_with_token, input_params.copy())


@pytest.mark.add_pull_request_reviewer
def test_add_pull_request_reviewer_invalid_pullRequestId(valid_credentials_with_token):
    input_params = params.get('add_pull_request_reviewer')[0].copy()
    input_params['pullRequestId'] = params.get('invalid_params')['text']
    with pytest.raises(ConnectorError):
        assert operations['add_pull_request_reviewer'](valid_credentials_with_token, input_params.copy())


@pytest.mark.list_pull_request_commits
@pytest.mark.parametrize("input_params", params['list_pull_request_commits'])
def test_list_pull_request_commits_success(valid_credentials_with_token, input_params):
    logger.info("params: {0}".format(input_params))
    assert operations['list_pull_request_commits'](valid_credentials_with_token, input_params.copy())


# Ensure that the provided input_params yield the correct output schema, or adjust the index in the list below.
# conditional_output_schema not supported.
@pytest.mark.list_pull_request_commits
@pytest.mark.schema_validation
def test_validate_list_pull_request_commits_output_schema(valid_credentials_with_token):
    input_params = params.get('list_pull_request_commits')[0]
    schema = {}
    for operation in info_json.get("operations"):
        if operation.get('operation') == 'list_pull_request_commits':
            if operation.get('conditional_output_schema'):
                schema = {}
            else:
                schema = operation.get('output_schema')
            break
    logger.info("output_schema: {0}".format(schema))
    assert set(
        operations['list_pull_request_commits'](valid_credentials_with_token, input_params.copy()).keys()) == set(
        schema.keys())


@pytest.mark.list_pull_request_commits
def test_list_pull_request_commits_invalid_pullRequestId(valid_credentials_with_token):
    input_params = params.get('list_pull_request_commits')[0].copy()
    input_params['pullRequestId'] = params.get('invalid_params')['text']
    with pytest.raises(ConnectorError):
        assert operations['list_pull_request_commits'](valid_credentials_with_token, input_params.copy())


@pytest.mark.list_pull_request_commits
def test_list_pull_request_commits_invalid_project(valid_credentials_with_token):
    input_params = params.get('list_pull_request_commits')[0].copy()
    input_params['project'] = params.get('invalid_params')['text']
    with pytest.raises(ConnectorError):
        assert operations['list_pull_request_commits'](valid_credentials_with_token, input_params.copy())


@pytest.mark.list_pull_request_commits
def test_list_pull_request_commits_invalid_repositoryId(valid_credentials_with_token):
    input_params = params.get('list_pull_request_commits')[0].copy()
    input_params['repositoryId'] = params.get('invalid_params')['text']
    with pytest.raises(ConnectorError):
        assert operations['list_pull_request_commits'](valid_credentials_with_token, input_params.copy())


@pytest.mark.list_commits
@pytest.mark.parametrize("input_params", params['list_commits'])
def test_list_commits_success(valid_credentials_with_token, input_params):
    logger.info("params: {0}".format(input_params))
    assert operations['list_commits'](valid_credentials_with_token, input_params.copy())


# Ensure that the provided input_params yield the correct output schema, or adjust the index in the list below.
# conditional_output_schema not supported.
@pytest.mark.list_commits
@pytest.mark.schema_validation
def test_validate_list_commits_output_schema(valid_credentials_with_token):
    input_params = params.get('list_commits')[0]
    schema = {}
    for operation in info_json.get("operations"):
        if operation.get('operation') == 'list_commits':
            if operation.get('conditional_output_schema'):
                schema = {}
            else:
                schema = operation.get('output_schema')
            break
    logger.info("output_schema: {0}".format(schema))
    assert set(operations['list_commits'](valid_credentials_with_token, input_params.copy()).keys()) == set(
        schema.keys())


@pytest.mark.list_commits
def test_list_commits_invalid_searchCriteria_ids(valid_credentials_with_token):
    input_params = params.get('list_commits')[0].copy()
    input_params['searchCriteria.ids'] = params.get('invalid_params')['text']
    with pytest.raises(ConnectorError):
        assert operations['list_commits'](valid_credentials_with_token, input_params.copy())


@pytest.mark.list_commits
def test_list_commits_invalid_project(valid_credentials_with_token):
    input_params = params.get('list_commits')[0].copy()
    input_params['project'] = params.get('invalid_params')['text']
    with pytest.raises(ConnectorError):
        assert operations['list_commits'](valid_credentials_with_token, input_params.copy())


@pytest.mark.list_commits
def test_list_commits_invalid_repositoryId(valid_credentials_with_token):
    input_params = params.get('list_commits')[0].copy()
    input_params['repositoryId'] = params.get('invalid_params')['text']
    with pytest.raises(ConnectorError):
        assert operations['list_commits'](valid_credentials_with_token, input_params.copy())


@pytest.mark.run_pipeline
@pytest.mark.parametrize("input_params", params['run_pipeline'])
def test_run_pipeline_success(valid_credentials_with_token, input_params):
    logger.info("params: {0}".format(input_params))
    assert operations['run_pipeline'](valid_credentials_with_token, input_params.copy())


# Ensure that the provided input_params yield the correct output schema, or adjust the index in the list below.
# conditional_output_schema not supported.
@pytest.mark.run_pipeline
@pytest.mark.schema_validation
def test_validate_run_pipeline_output_schema(valid_credentials_with_token):
    input_params = params.get('run_pipeline')[0]
    schema = {}
    for operation in info_json.get("operations"):
        if operation.get('operation') == 'run_pipeline':
            if operation.get('conditional_output_schema'):
                schema = {
                    "id": "",
                    "url": "",
                    "name": "",
                    "state": "",
                    "_links": {
                        "web": {
                            "href": ""
                        },
                        "self": {
                            "href": ""
                        },
                        "pipeline": {
                            "href": ""
                        },
                        "pipeline.web": {
                            "href": ""
                        }
                    },
                    "pipeline": {
                        "id": "",
                        "url": "",
                        "name": "",
                        "folder": "",
                        "revision": ""
                    },
                    "resources": {
                        "repositories": {
                            "self": {
                                "refName": "",
                                "version": "",
                                "repository": {
                                    "id": "",
                                    "type": ""
                                }
                            }
                        }
                    },
                    "createdDate": "",
                    "templateParameters": {}
                }
            else:
                schema = operation.get('output_schema')
            break
    logger.info("output_schema: {0}".format(schema))
    assert set(operations['run_pipeline'](valid_credentials_with_token, input_params.copy()).keys()) == set(
        schema.keys())


@pytest.mark.run_pipeline
def test_run_pipeline_invalid_stagesToSkip(valid_credentials_with_token):
    input_params = params.get('run_pipeline')[0].copy()
    input_params['stagesToSkip'] = params.get('invalid_params')['text']
    with pytest.raises(ConnectorError):
        assert operations['run_pipeline'](valid_credentials_with_token, input_params.copy())


@pytest.mark.run_pipeline
def test_run_pipeline_invalid_project(valid_credentials_with_token):
    input_params = params.get('run_pipeline')[0].copy()
    input_params['project'] = params.get('invalid_params')['text']
    with pytest.raises(ConnectorError):
        assert operations['run_pipeline'](valid_credentials_with_token, input_params.copy())


@pytest.mark.run_pipeline
def test_run_pipeline_invalid_pipelineId(valid_credentials_with_token):
    input_params = params.get('run_pipeline')[0].copy()
    input_params['pipelineId'] = params.get('invalid_params')['integer']
    with pytest.raises(ConnectorError):
        assert operations['run_pipeline'](valid_credentials_with_token, input_params.copy())


@pytest.mark.run_pipeline
def test_run_pipeline_invalid_pipelineVersion(valid_credentials_with_token):
    input_params = params.get('run_pipeline')[0].copy()
    input_params['pipelineVersion'] = params.get('invalid_params')['integer']
    with pytest.raises(ConnectorError):
        assert operations['run_pipeline'](valid_credentials_with_token, input_params.copy())
