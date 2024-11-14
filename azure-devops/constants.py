"""
Copyright start
MIT License
Copyright (c) 2024 Fortinet Inc
Copyright end
"""


# redirect url
DEFAULT_REDIRECT_URL = 'https://localhost/myapp'
REFRESH_TOKEN_FLAG = False
AUTHORIZATION_CODE = 'authorization_code'
REFRESH_TOKEN = 'refresh_token'
API_VERSION = '7.1'
CONFIG_SUPPORTS_TOKEN = True

PROJECT_STATE_MAPPING = {
    "All": "all",
    "Create Pending": "createPending",
    "Deleted": "deleted",
    "Deleting": "deleting",
    "New": "new",
    "Unchanged": "unchanged",
    "Well Formed": "wellFormed"
}

PR_STATUS_MAPPING = {
    "All": "all",
    "Active": "active",
    "Abandoned": "abandoned",
    "Completed": "completed",
    "Not Set": "notSet"
}

REVIEWER_PAYLOAD = {
        "query": "",
        "identityTypes": [
            "user"
        ],
        "operationScopes": [
            "ims",
            "source"
        ],
        "options": {
            "MinResults": 5,
            "MaxResults": 40
        },
        "properties": [
            "DisplayName",
            "IsMru",
            "ScopeName",
            "SamAccountName",
            "Active",
            "SubjectDescriptor",
            "Department",
            "JobTitle",
            "Mail",
            "MailNickname",
            "PhysicalDeliveryOfficeName",
            "SignInAddress",
            "Surname",
            "Guest",
            "TelephoneNumber",
            "Manager",
            "Description"
        ]
    }
