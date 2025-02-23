import requests
import json
from requests.auth import HTTPBasicAuth


jira_url = "https://viziontech.atlassian.net/rest/api/3/project"
user_email = "hammadullahris@gmail.com"

api_token = open(".env", 'r').readline().split()[0]#.split("=")[1].strip().strip('\n')


auth = HTTPBasicAuth(user_email, api_token)

headers = {"Accept": "application/json", "Content-Type": "application/json"}

response = requests.request(
    "GET",
    jira_url,
    headers=headers,
    auth=auth
)

projects = json.loads(response.text) #json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": "))

for project in projects:
    print(project['key'])
    key = project['key']
    url = f"https://viziontech.atlassian.net/rest/api/3/search?jql=project={key}&maxResult=1000"
    response = requests.request(
        "GET",
        url,
        headers=headers,
        auth=auth
        )
    issues = json.loads(response.text)
    print(issues)

