from requests import request
import json
from requests.auth import HTTPBasicAuth
import traceback

tb_on = True
jira_url = "https://viziontech.atlassian.net/rest/api/3/project"

base_url = "https://viziontech.atlassian.net"
user_email = "hammadullahris@gmail.com"

api_token = open(".env", 'r').readline().split()[0]  # .split("=")[1].strip().strip('\n')

auth = HTTPBasicAuth(user_email, api_token)

headers = {"Accept": "application/json", "Content-Type": "application/json"}


def getAllProjects():
    try:
        global base_url, auth, headers
        url = f"{base_url}/rest/api/3/project"
        response = request("GET", url, headers=headers, auth=auth)
        projects = json.loads(
            response.text)  # json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": "))
        for project in projects:
            getProjectIssues(project)
    except Exception as e:
        traces()
        print(f"Something bad happened: {e}")


def getProjectIssues(project):
    '''Get all the issues in the project and return json object'''
    global auth, headers
    key = project['key']
    url = f"{base_url}/rest/api/3/search?jql=project={key}&maxResult=1000"
    response = request("GET", url, headers=headers, auth=auth)
    # print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
    return json.loads(response.text)


def getProject(projectkey):
    '''Provides project in json format'''
    global base_url, auth, headers
    url = f"{base_url}/rest/api/3/project/{projectkey}"
    response = request("GET", url, headers=headers, auth=auth)
    project = getProjectIssues(json.loads(response.text))
    return project


def jsonDump(payload):
    return json.dumps(payload, sort_keys=True, indent=4, separators=(",", ": "))


# for issue in project['issues']:
# print(issue.key)

def progressOfIssues(issues):
    for issue in issues:
        fields = issue['fields']
        #print(jsonDump(fields))
        print(f"issue number= {issue['key']}\nissue summary={fields['summary']}\nprogress={fields['status']['name']}\nAssigned to: {fields['assignee']['displayName'] if fields['assignee'] else fields['assignee']}")
        print()


progressOfIssues(getProject("SM")['issues'])


def traces():
    global tb_on
    if tb_on:
        tb = traceback.format_exc()
        print(f"traces {tb}")

# getAllProjects()
