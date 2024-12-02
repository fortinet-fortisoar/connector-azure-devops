# Edit the config_and_params.json file and add the necessary parameter values.
# Ensure that the provided input_params yield the correct output schema.
# Add logic for validating conditional_output_schema or if schema is other than dict.
# Add any specific assertions in each test case, based on the expected response.

"""
Copyright start
MIT License
Copyright (c) 2024 Fortinet Inc
Copyright end
"""

import pytest
import logging
logger = logging.getLogger(__name__)
from testframework.conftest import valid_configuration, invalid_configuration, valid_configuration_with_token,\
    connector_id, connector_details, info_json, params_json
from testframework.helpers.test_helpers import run_health_check_success, run_invalid_config_test, run_success_test,\
    run_output_schema_validation, run_invalid_param_test, set_report_metadata
    

@pytest.mark.check_health
def test_check_health_success(valid_configuration, connector_details):
    set_report_metadata(connector_details, "Health Check", "Verify with valid Configuration")
    result = run_health_check_success(valid_configuration, connector_details)
    assert result.get('status') == 'Available'
    

@pytest.mark.check_health
def test_check_health_invalid_api_key(invalid_configuration, connector_id, connector_details, params_json):
    set_report_metadata(connector_details, "Health Check", "Verify with invalid Access Token")
    result = run_invalid_config_test(invalid_configuration, connector_id, connector_details, param_name='api_key',
                                     param_type='password', config=params_json['config'])
    assert result.get('status') == "Disconnected"
    

@pytest.mark.check_health
def test_check_health_invalid_api_version(invalid_configuration, connector_id, connector_details, params_json):
    set_report_metadata(connector_details, "Health Check", "Verify with invalid API Version")
    result = run_invalid_config_test(invalid_configuration, connector_id, connector_details, param_name='api_version',
                                     param_type='text', config=params_json['config'])
    assert result.get('status') == "Disconnected"
    

@pytest.mark.check_health
def test_check_health_invalid_organization(invalid_configuration, connector_id, connector_details, params_json):
    set_report_metadata(connector_details, "Health Check", "Verify with invalid Organization Name")
    result = run_invalid_config_test(invalid_configuration, connector_id, connector_details, param_name='organization',
                                     param_type='text', config=params_json['config'])
    assert result.get('status') == "Disconnected"
    

@pytest.mark.check_health
def test_check_health_invalid_server_url(invalid_configuration, connector_id, connector_details, params_json):
    set_report_metadata(connector_details, "Health Check", "Verify with invalid Server URL")
    result = run_invalid_config_test(invalid_configuration, connector_id, connector_details, param_name='server_url',
                                     param_type='text', config=params_json['config'])
    assert result.get('status') == "Disconnected"
    

@pytest.mark.list_pipelines
def test_list_pipelines_success(cache, valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get Pipeline List", "Verify with valid Input Parameters")
    for result in run_success_test(cache, connector_details, operation_name='list_pipelines',
                                   action_params=params_json['list_pipelines']):
        assert result.get('status') == "Success"
        pipelines = result.get('data', {}).get('value')
        if pipelines:
            params_json['run_pipeline'][0]['pipelineId'] = pipelines[0]['id']


@pytest.mark.list_pipelines
def test_validate_list_pipelines_output_schema(cache, valid_configuration_with_token, connector_details,
                                                 info_json, params_json):
    set_report_metadata(connector_details, "Get Pipeline List", "Validate Output Schema")
    run_output_schema_validation(cache, 'list_pipelines', info_json, params_json['list_pipelines'])
    

@pytest.mark.list_pipelines
def test_list_pipelines_invalid_project(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get Pipeline List", "Verify with invalid Project Name")
    result = run_invalid_param_test(connector_details, operation_name='list_pipelines', param_name='project',
                                    param_type='text', action_params=params_json['list_pipelines'])
    assert result.get('status') == "failed"


@pytest.mark.run_pipeline
def test_run_pipeline_success(cache, valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Run Pipeline", "Verify with valid Input Parameters")
    for result in run_success_test(cache, connector_details, operation_name='run_pipeline',
                                   action_params=params_json['run_pipeline']):
        assert result.get('status') == "Success"


@pytest.mark.run_pipeline
def test_validate_run_pipeline_output_schema(cache, valid_configuration_with_token, connector_details,
                                                 info_json, params_json):
    set_report_metadata(connector_details, "Run Pipeline", "Validate Output Schema")
    run_output_schema_validation(cache, 'run_pipeline', info_json, params_json['run_pipeline'])


@pytest.mark.run_pipeline
def test_run_pipeline_invalid_stagestoskip(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Run Pipeline", "Verify with invalid Stages to Skip")
    result = run_invalid_param_test(connector_details, operation_name='run_pipeline', param_name='stagesToSkip',
                                    param_type='text', action_params=params_json['run_pipeline'])
    assert result.get('status') == "failed"


@pytest.mark.list_pipeline_runs
def test_list_pipeline_runs_success(cache, valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get Pipeline Run List", "Verify with valid Input Parameters")
    for result in run_success_test(cache, connector_details, operation_name='list_pipeline_runs',
                                   action_params=params_json['list_pipeline_runs']):
        assert result.get('status') == "Success"
        print("\n\nlist_pipeline_runs result: {0}\n\n".format(result))
        for pipeline_run in result.get('data', {}).get('value'):
            logger.info("\n\nlist_pipeline_runs: {0}\n\n".format(pipeline_run))
            params_json['get_pipeline_run'][0]['pipelineId'] = pipeline_run.get('pipeline').get('id')
            params_json['get_pipeline_run'][0]['runId'] = pipeline_run.get('id')


@pytest.mark.list_pipeline_runs
def test_validate_list_pipeline_runs_output_schema(cache, valid_configuration_with_token, connector_details,
                                                 info_json, params_json):
    set_report_metadata(connector_details, "Get Pipeline Run List", "Validate Output Schema")
    run_output_schema_validation(cache, 'list_pipeline_runs', info_json, params_json['list_pipeline_runs'])
    

@pytest.mark.list_pipeline_runs
def test_list_pipeline_runs_invalid_project(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get Pipeline Run List", "Verify with invalid Project Name")
    result = run_invalid_param_test(connector_details, operation_name='list_pipeline_runs', param_name='project',
                                    param_type='text', action_params=params_json['list_pipeline_runs'])
    assert result.get('status') == "failed"
    

@pytest.mark.list_pipeline_runs
def test_list_pipeline_runs_invalid_pipelineid(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get Pipeline Run List", "Verify with invalid Pipeline ID")
    result = run_invalid_param_test(connector_details, operation_name='list_pipeline_runs', param_name='pipelineId',
                                    param_type='integer', action_params=params_json['list_pipeline_runs'])
    assert result.get('status') == "failed"
    

@pytest.mark.get_pipeline_run
def test_get_pipeline_run_success(cache, valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get Pipeline Run Details", "Verify with valid Input Parameters")
    for result in run_success_test(cache, connector_details, operation_name='get_pipeline_run',
                                   action_params=params_json['get_pipeline_run']):
        assert result.get('status') == "Success"


@pytest.mark.get_pipeline_run
def test_validate_get_pipeline_run_output_schema(cache, valid_configuration_with_token, connector_details,
                                                 info_json, params_json):
    set_report_metadata(connector_details, "Get Pipeline Run Details", "Validate Output Schema")
    run_output_schema_validation(cache, 'get_pipeline_run', info_json, params_json['get_pipeline_run'])
    

@pytest.mark.get_pipeline_run
def test_get_pipeline_run_invalid_project(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get Pipeline Run Details", "Verify with invalid Project Name")
    result = run_invalid_param_test(connector_details, operation_name='get_pipeline_run', param_name='project',
                                    param_type='text', action_params=params_json['get_pipeline_run'])
    assert result.get('status') == "failed"
    

@pytest.mark.get_pipeline_run
def test_get_pipeline_run_invalid_runid(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get Pipeline Run Details", "Verify with invalid Run ID")
    result = run_invalid_param_test(connector_details, operation_name='get_pipeline_run', param_name='runId',
                                    param_type='text', action_params=params_json['get_pipeline_run'])
    assert result.get('status') == "failed"
    

@pytest.mark.get_pipeline_run
def test_get_pipeline_run_invalid_pipelineid(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get Pipeline Run Details", "Verify with invalid Pipeline ID")
    result = run_invalid_param_test(connector_details, operation_name='get_pipeline_run', param_name='pipelineId',
                                    param_type='integer', action_params=params_json['get_pipeline_run'])
    assert result.get('status') == "failed"
    

@pytest.mark.list_projects
def test_list_projects_success(cache, valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get Project List", "Verify with valid Input Parameters")
    for result in run_success_test(cache, connector_details, operation_name='list_projects',
                                   action_params=params_json['list_projects']):
        assert result.get('status') == "Success"


@pytest.mark.list_projects
def test_validate_list_projects_output_schema(cache, valid_configuration_with_token, connector_details,
                                                 info_json, params_json):
    set_report_metadata(connector_details, "Get Project List", "Validate Output Schema")
    run_output_schema_validation(cache, 'list_projects', info_json, params_json['list_projects'])


@pytest.mark.list_repositories
def test_list_repositories_success(cache, valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get Repository List", "Verify with valid Input Parameters")
    for result in run_success_test(cache, connector_details, operation_name='list_repositories',
                                   action_params=params_json['list_repositories']):
        assert result.get('status') == "Success"


@pytest.mark.list_repositories
def test_validate_list_repositories_output_schema(cache, valid_configuration_with_token, connector_details,
                                                 info_json, params_json):
    set_report_metadata(connector_details, "Get Repository List", "Validate Output Schema")
    run_output_schema_validation(cache, 'list_repositories', info_json, params_json['list_repositories'])
    

@pytest.mark.list_repositories
def test_list_repositories_invalid_project(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get Repository List", "Verify with invalid Project Name")
    result = run_invalid_param_test(connector_details, operation_name='list_repositories', param_name='project',
                                    param_type='text', action_params=params_json['list_repositories'])
    assert result.get('status') == "failed"
    

@pytest.mark.list_branches
def test_list_branches_success(cache, valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get Branch List", "Verify with valid Input Parameters")
    for result in run_success_test(cache, connector_details, operation_name='list_branches',
                                   action_params=params_json['list_branches']):
        assert result.get('status') == "Success"


@pytest.mark.list_branches
def test_validate_list_branches_output_schema(cache, valid_configuration_with_token, connector_details,
                                                 info_json, params_json):
    set_report_metadata(connector_details, "Get Branch List", "Validate Output Schema")
    run_output_schema_validation(cache, 'list_branches', info_json, params_json['list_branches'])


@pytest.mark.list_branches
def test_list_branches_invalid_repository(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get Branch List", "Verify with invalid Repository")
    result = run_invalid_param_test(connector_details, operation_name='list_branches', param_name='repository',
                                    param_type='text', action_params=params_json['list_branches'])
    assert result.get('status') == "failed"
    

@pytest.mark.list_branches
def test_list_branches_invalid_project(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get Branch List", "Verify with invalid Project Name")
    result = run_invalid_param_test(connector_details, operation_name='list_branches', param_name='project',
                                    param_type='text', action_params=params_json['list_branches'])
    assert result.get('status') == "failed"


@pytest.mark.list_branches
def test_list_branches_invalid_filter(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get Branch List", "Verify with invalid Branch Name Filter (Starts With)")
    result = run_invalid_param_test(connector_details, operation_name='list_branches', param_name='filter',
                                    param_type='text', action_params=params_json['list_branches'])
    assert result.get('status') == "failed"


@pytest.mark.list_branches
def test_list_branches_invalid_filtercontains(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get Branch List", "Verify with invalid Branch Name Filter (Contains)")
    result = run_invalid_param_test(connector_details, operation_name='list_branches', param_name='filterContains',
                                    param_type='text', action_params=params_json['list_branches'])
    assert result.get('status') == "failed"
    

@pytest.mark.get_commit
def test_get_commit_success(cache, valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get Commit Details", "Verify with valid Input Parameters")
    for result in run_success_test(cache, connector_details, operation_name='get_commit',
                                   action_params=params_json['get_commit']):
        assert result.get('status') == "Success"


@pytest.mark.get_commit
def test_validate_get_commit_output_schema(cache, valid_configuration_with_token, connector_details,
                                                 info_json, params_json):
    set_report_metadata(connector_details, "Get Commit Details", "Validate Output Schema")
    # run_output_schema_validation(cache, 'get_commit', info_json, params_json['get_commit'])
    assert _validate_json_schema(cache, 'get_commit', info_json)

@pytest.mark.get_commit
def test_get_commit_invalid_project(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get Commit Details", "Verify with invalid Project Name")
    result = run_invalid_param_test(connector_details, operation_name='get_commit', param_name='project',
                                    param_type='text', action_params=params_json['get_commit'])
    assert result.get('status') == "failed"
    

@pytest.mark.get_commit
def test_get_commit_invalid_commitid(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get Commit Details", "Verify with invalid Commit ID")
    result = run_invalid_param_test(connector_details, operation_name='get_commit', param_name='commitId',
                                    param_type='text', action_params=params_json['get_commit'])
    assert result.get('status') == "failed"
    

@pytest.mark.get_commit
def test_get_commit_invalid_repositoryid(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get Commit Details", "Verify with invalid Repository")
    result = run_invalid_param_test(connector_details, operation_name='get_commit', param_name='repositoryId',
                                    param_type='text', action_params=params_json['get_commit'])
    assert result.get('status') == "failed"

####################################
####################################
####################################
####################################


@pytest.mark.create_pull_request
def test_create_pull_request_success(cache, valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Create Pull Request", "Verify with valid Input Parameters")
    for result in run_success_test(cache, connector_details, operation_name='create_pull_request',
                                   action_params=params_json['create_pull_request']):
        assert result.get('status') == "Success"
        pull_request_id = result.get('data', {}).get('pullRequestId')
        if pull_request_id:
            params_json.get('update_pull_request')[0]['pullRequestId'] = pull_request_id
            params_json.get('get_pull_requests_by_id')[0]['pullRequestId'] = pull_request_id
            params_json.get('list_pull_request_reviewers')[0]['pullRequestId'] = pull_request_id
            params_json.get('add_pull_request_reviewer')[0]['pullRequestId'] = pull_request_id
            params_json.get('list_pull_request_commits')[0]['pullRequestId'] = pull_request_id


@pytest.mark.create_pull_request
def test_validate_create_pull_request_output_schema(cache, valid_configuration_with_token, connector_details,
                                                    info_json, params_json):
    set_report_metadata(connector_details, "Create Pull Request", "Validate Output Schema")
    run_output_schema_validation(cache, 'create_pull_request', info_json, params_json['create_pull_request'])


@pytest.mark.create_pull_request
def test_create_pull_request_invalid_title(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Create Pull Request", "Verify with invalid Pull Request Title")
    result = run_invalid_param_test(connector_details, operation_name='create_pull_request', param_name='title',
                                    param_type='text', action_params=params_json['create_pull_request'])
    assert result.get('status') == "failed"


@pytest.mark.create_pull_request
def test_create_pull_request_invalid_repositoryid(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Create Pull Request", "Verify with invalid Repository")
    result = run_invalid_param_test(connector_details, operation_name='create_pull_request', param_name='repositoryId',
                                    param_type='text', action_params=params_json['create_pull_request'])
    assert result.get('status') == "failed"


@pytest.mark.create_pull_request
def test_create_pull_request_invalid_additional_input(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Create Pull Request", "Verify with invalid Additional Inputs")
    result = run_invalid_param_test(connector_details, operation_name='create_pull_request',
                                    param_name='additional_input',
                                    param_type='json', action_params=params_json['create_pull_request'])
    assert result.get('status') == "failed"


@pytest.mark.create_pull_request
def test_create_pull_request_invalid_reviewers(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Create Pull Request", "Verify with invalid Reviewers")
    result = run_invalid_param_test(connector_details, operation_name='create_pull_request', param_name='reviewers',
                                    param_type='text', action_params=params_json['create_pull_request'])
    assert result.get('status') == "failed"


@pytest.mark.create_pull_request
def test_create_pull_request_invalid_project(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Create Pull Request", "Verify with invalid Project Name")
    result = run_invalid_param_test(connector_details, operation_name='create_pull_request', param_name='project',
                                    param_type='text', action_params=params_json['create_pull_request'])
    assert result.get('status') == "failed"


@pytest.mark.create_pull_request
def test_create_pull_request_invalid_targetrefname(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Create Pull Request", "Verify with invalid Target Branch Name")
    result = run_invalid_param_test(connector_details, operation_name='create_pull_request', param_name='targetRefName',
                                    param_type='text', action_params=params_json['create_pull_request'])
    assert result.get('status') == "failed"


@pytest.mark.create_pull_request
def test_create_pull_request_invalid_sourcerefname(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Create Pull Request", "Verify with invalid Source Branch Name")
    result = run_invalid_param_test(connector_details, operation_name='create_pull_request', param_name='sourceRefName',
                                    param_type='text', action_params=params_json['create_pull_request'])
    assert result.get('status') == "failed"


@pytest.mark.list_pull_requests
def test_list_pull_requests_success(cache, valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get Pull Request List", "Verify with valid Input Parameters")
    for result in run_success_test(cache, connector_details, operation_name='list_pull_requests',
                                   action_params=params_json['list_pull_requests']):
        assert result.get('status') == "Success"


@pytest.mark.list_pull_requests
def test_validate_list_pull_requests_output_schema(cache, valid_configuration_with_token, connector_details,
                                                 info_json, params_json):
    set_report_metadata(connector_details, "Get Pull Request List", "Validate Output Schema")
    run_output_schema_validation(cache, 'list_pull_requests', info_json, params_json['list_pull_requests'])
    

@pytest.mark.list_pull_requests
def test_list_pull_requests_invalid_repositoryid(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get Pull Request List", "Verify with invalid Repository")
    result = run_invalid_param_test(connector_details, operation_name='list_pull_requests', param_name='repositoryId',
                                    param_type='text', action_params=params_json['list_pull_requests'])
    assert result.get('status') == "failed"


@pytest.mark.list_pull_requests
def test_list_pull_requests_invalid_project(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get Pull Request List", "Verify with invalid Project Name")
    result = run_invalid_param_test(connector_details, operation_name='list_pull_requests', param_name='project',
                                    param_type='text', action_params=params_json['list_pull_requests'])
    assert result.get('status') == "failed"


@pytest.mark.get_pull_requests_by_id
def test_get_pull_requests_by_id_success(cache, valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get Pull Request Details", "Verify with valid Input Parameters")
    for result in run_success_test(cache, connector_details, operation_name='get_pull_requests_by_id',
                                   action_params=params_json['get_pull_requests_by_id']):
        assert result.get('status') == "Success"


@pytest.mark.get_pull_requests_by_id
def test_validate_get_pull_requests_by_id_output_schema(cache, valid_configuration_with_token, connector_details,
                                                 info_json, params_json):
    set_report_metadata(connector_details, "Get Pull Request Details", "Validate Output Schema")
    run_output_schema_validation(cache, 'get_pull_requests_by_id', info_json, params_json['get_pull_requests_by_id'])
    

@pytest.mark.get_pull_requests_by_id
def test_get_pull_requests_by_id_invalid_project(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get Pull Request Details", "Verify with invalid Project Name")
    result = run_invalid_param_test(connector_details, operation_name='get_pull_requests_by_id', param_name='project',
                                    param_type='text', action_params=params_json['get_pull_requests_by_id'])
    assert result.get('status') == "failed"
    

@pytest.mark.get_pull_requests_by_id
def test_get_pull_requests_by_id_invalid_pullrequestid(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get Pull Request Details", "Verify with invalid Pull Request ID")
    result = run_invalid_param_test(connector_details, operation_name='get_pull_requests_by_id', param_name='pullRequestId',
                                    param_type='integer', action_params=params_json['get_pull_requests_by_id'])
    assert result.get('status') == "failed"
    

@pytest.mark.update_pull_request
def test_update_pull_request_success(cache, valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Update Pull Request", "Verify with valid Input Parameters")
    for result in run_success_test(cache, connector_details, operation_name='update_pull_request',
                                   action_params=params_json['update_pull_request']):
        assert result.get('status') == "Success"


@pytest.mark.update_pull_request
def test_validate_update_pull_request_output_schema(cache, valid_configuration_with_token, connector_details,
                                                 info_json, params_json):
    set_report_metadata(connector_details, "Update Pull Request", "Validate Output Schema")
    run_output_schema_validation(cache, 'update_pull_request', info_json, params_json['update_pull_request'])


@pytest.mark.update_pull_request
def test_update_pull_request_invalid_repositoryid(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Update Pull Request", "Verify with invalid Repository")
    result = run_invalid_param_test(connector_details, operation_name='update_pull_request', param_name='repositoryId',
                                    param_type='text', action_params=params_json['update_pull_request'])
    assert result.get('status') == "failed"


@pytest.mark.update_pull_request
def test_update_pull_request_invalid_project(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Update Pull Request", "Verify with invalid Project Name")
    result = run_invalid_param_test(connector_details, operation_name='update_pull_request', param_name='project',
                                    param_type='text', action_params=params_json['update_pull_request'])
    assert result.get('status') == "failed"
    

@pytest.mark.update_pull_request
def test_update_pull_request_invalid_pullrequestid(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Update Pull Request", "Verify with invalid Pull Request ID")
    result = run_invalid_param_test(connector_details, operation_name='update_pull_request', param_name='pullRequestId',
                                    param_type='text', action_params=params_json['update_pull_request'])
    assert result.get('status') == "failed"
    

@pytest.mark.update_pull_request
def test_update_pull_request_invalid_targetrefname(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Update Pull Request", "Verify with invalid Target Branch Name")
    result = run_invalid_param_test(connector_details, operation_name='update_pull_request', param_name='targetRefName',
                                    param_type='text', action_params=params_json['update_pull_request'])
    assert result.get('status') == "failed"
    

@pytest.mark.list_pull_request_reviewers
def test_list_pull_request_reviewers_success(cache, valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get Pull Request Reviewer List", "Verify with valid Input Parameters")
    for result in run_success_test(cache, connector_details, operation_name='list_pull_request_reviewers',
                                   action_params=params_json['list_pull_request_reviewers']):
        assert result.get('status') == "Success"


@pytest.mark.list_pull_request_reviewers
def test_validate_list_pull_request_reviewers_output_schema(cache, valid_configuration_with_token, connector_details,
                                                 info_json, params_json):
    set_report_metadata(connector_details, "Get Pull Request Reviewer List", "Validate Output Schema")
    run_output_schema_validation(cache, 'list_pull_request_reviewers', info_json, params_json['list_pull_request_reviewers'])
    

@pytest.mark.list_pull_request_reviewers
def test_list_pull_request_reviewers_invalid_project(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get Pull Request Reviewer List", "Verify with invalid Project Name")
    result = run_invalid_param_test(connector_details, operation_name='list_pull_request_reviewers', param_name='project',
                                    param_type='text', action_params=params_json['list_pull_request_reviewers'])
    assert result.get('status') == "failed"
    

@pytest.mark.list_pull_request_reviewers
def test_list_pull_request_reviewers_invalid_pullrequestid(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get Pull Request Reviewer List", "Verify with invalid Pull Request ID")
    result = run_invalid_param_test(connector_details, operation_name='list_pull_request_reviewers', param_name='pullRequestId',
                                    param_type='text', action_params=params_json['list_pull_request_reviewers'])
    assert result.get('status') == "failed"
    

@pytest.mark.list_pull_request_reviewers
def test_list_pull_request_reviewers_invalid_repositoryid(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get Pull Request Reviewer List", "Verify with invalid Repository")
    result = run_invalid_param_test(connector_details, operation_name='list_pull_request_reviewers', param_name='repositoryId',
                                    param_type='text', action_params=params_json['list_pull_request_reviewers'])
    assert result.get('status') == "failed"
    

@pytest.mark.add_pull_request_reviewer
def test_add_pull_request_reviewer_success(cache, valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Add Pull Request Reviewer", "Verify with valid Input Parameters")
    for result in run_success_test(cache, connector_details, operation_name='add_pull_request_reviewer',
                                   action_params=params_json['add_pull_request_reviewer']):
        assert result.get('status') == "Success"


@pytest.mark.add_pull_request_reviewer
def test_validate_add_pull_request_reviewer_output_schema(cache, valid_configuration_with_token, connector_details,
                                                 info_json, params_json):
    set_report_metadata(connector_details, "Add Pull Request Reviewer", "Validate Output Schema")
    run_output_schema_validation(cache, 'add_pull_request_reviewer', info_json, params_json['add_pull_request_reviewer'])
    

@pytest.mark.add_pull_request_reviewer
def test_add_pull_request_reviewer_invalid_reviewerid(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Add Pull Request Reviewer", "Verify with invalid Reviewer")
    result = run_invalid_param_test(connector_details, operation_name='add_pull_request_reviewer', param_name='reviewerId',
                                    param_type='text', action_params=params_json['add_pull_request_reviewer'])
    assert result.get('status') == "failed"
    

@pytest.mark.add_pull_request_reviewer
def test_add_pull_request_reviewer_invalid_repositoryid(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Add Pull Request Reviewer", "Verify with invalid Repository")
    result = run_invalid_param_test(connector_details, operation_name='add_pull_request_reviewer', param_name='repositoryId',
                                    param_type='text', action_params=params_json['add_pull_request_reviewer'])
    assert result.get('status') == "failed"
    

@pytest.mark.add_pull_request_reviewer
def test_add_pull_request_reviewer_invalid_pullrequestid(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Add Pull Request Reviewer", "Verify with invalid Pull Request ID")
    result = run_invalid_param_test(connector_details, operation_name='add_pull_request_reviewer', param_name='pullRequestId',
                                    param_type='text', action_params=params_json['add_pull_request_reviewer'])
    assert result.get('status') == "failed"
    

@pytest.mark.add_pull_request_reviewer
def test_add_pull_request_reviewer_invalid_project(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Add Pull Request Reviewer", "Verify with invalid Project Name")
    result = run_invalid_param_test(connector_details, operation_name='add_pull_request_reviewer', param_name='project',
                                    param_type='text', action_params=params_json['add_pull_request_reviewer'])
    assert result.get('status') == "failed"
    

@pytest.mark.list_pull_request_commits
def test_list_pull_request_commits_success(cache, valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get Pull Request Commit List", "Verify with valid Input Parameters")
    for result in run_success_test(cache, connector_details, operation_name='list_pull_request_commits',
                                   action_params=params_json['list_pull_request_commits']):
        assert result.get('status') == "Success"


@pytest.mark.list_pull_request_commits
def test_validate_list_pull_request_commits_output_schema(cache, valid_configuration_with_token, connector_details,
                                                 info_json, params_json):
    set_report_metadata(connector_details, "Get Pull Request Commit List", "Validate Output Schema")
    run_output_schema_validation(cache, 'list_pull_request_commits', info_json, params_json['list_pull_request_commits'])
    

@pytest.mark.list_pull_request_commits
def test_list_pull_request_commits_invalid_repositoryid(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get Pull Request Commit List", "Verify with invalid Repository")
    result = run_invalid_param_test(connector_details, operation_name='list_pull_request_commits', param_name='repositoryId',
                                    param_type='text', action_params=params_json['list_pull_request_commits'])
    assert result.get('status') == "failed"
    

@pytest.mark.list_pull_request_commits
def test_list_pull_request_commits_invalid_continuationtoken(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get Pull Request Commit List", "Verify with invalid Continuation Token")
    result = run_invalid_param_test(connector_details, operation_name='list_pull_request_commits', param_name='continuationToken',
                                    param_type='text', action_params=params_json['list_pull_request_commits'])
    assert result.get('status') == "failed"
    

@pytest.mark.list_pull_request_commits
def test_list_pull_request_commits_invalid_project(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get Pull Request Commit List", "Verify with invalid Project Name")
    result = run_invalid_param_test(connector_details, operation_name='list_pull_request_commits', param_name='project',
                                    param_type='text', action_params=params_json['list_pull_request_commits'])
    assert result.get('status') == "failed"
    

@pytest.mark.list_pull_request_commits
def test_list_pull_request_commits_invalid_pullrequestid(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get Pull Request Commit List", "Verify with invalid Pull Request ID")
    result = run_invalid_param_test(connector_details, operation_name='list_pull_request_commits', param_name='pullRequestId',
                                    param_type='text', action_params=params_json['list_pull_request_commits'])
    assert result.get('status') == "failed"
    

@pytest.mark.list_commits
def test_list_commits_success(cache, valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get Commit List", "Verify with valid Input Parameters")
    for result in run_success_test(cache, connector_details, operation_name='list_commits',
                                   action_params=params_json['list_commits']):
        assert result.get('status') == "Success"


@pytest.mark.list_commits
def test_validate_list_commits_output_schema(cache, valid_configuration_with_token, connector_details,
                                                 info_json, params_json):
    set_report_metadata(connector_details, "Get Commit List", "Validate Output Schema")
    run_output_schema_validation(cache, 'list_commits', info_json, params_json['list_commits'])
    

@pytest.mark.list_commits
def test_list_commits_invalid_project(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get Commit List", "Verify with invalid Project Name")
    result = run_invalid_param_test(connector_details, operation_name='list_commits', param_name='project',
                                    param_type='text', action_params=params_json['list_commits'])
    assert result.get('status') == "failed"
    

@pytest.mark.list_commits
def test_list_commits_invalid_searchcriteria_ids(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get Commit List", "Verify with invalid Commit IDs")
    result = run_invalid_param_test(connector_details, operation_name='list_commits', param_name='searchCriteria.ids',
                                    param_type='text', action_params=params_json['list_commits'])
    assert result.get('status') == "failed"
    

@pytest.mark.list_commits
def test_list_commits_invalid_repositoryid(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get Commit List", "Verify with invalid Repository")
    result = run_invalid_param_test(connector_details, operation_name='list_commits', param_name='repositoryId',
                                    param_type='text', action_params=params_json['list_commits'])
    assert result.get('status') == "failed"
    

@pytest.mark.run_pipeline
def test_run_pipeline_invalid_project(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Run Pipeline", "Verify with invalid Project Name")
    result = run_invalid_param_test(connector_details, operation_name='run_pipeline', param_name='project',
                                    param_type='text', action_params=params_json['run_pipeline'])
    assert result.get('status') == "failed"
    

@pytest.mark.run_pipeline
def test_run_pipeline_invalid_pipelineversion(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Run Pipeline", "Verify with invalid Pipeline Version")
    result = run_invalid_param_test(connector_details, operation_name='run_pipeline', param_name='pipelineVersion',
                                    param_type='integer', action_params=params_json['run_pipeline'])
    assert result.get('status') == "failed"
    

@pytest.mark.run_pipeline
def test_run_pipeline_invalid_pipelineid(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Run Pipeline", "Verify with invalid Pipeline ID")
    result = run_invalid_param_test(connector_details, operation_name='run_pipeline', param_name='pipelineId',
                                    param_type='integer', action_params=params_json['run_pipeline'])
    assert result.get('status') == "failed"
