from requests import request
import json
from requests.auth import HTTPBasicAuth
import traceback


def getAllProjects():
    try:
        global base_url, auth, headers
        url = f"{base_url}/rest/api/3/project"
        response = request("GET", url, headers=headers, auth=auth)
        projects = response.json()  # json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": "))
        projectObj = []
        for project in projects:
            projectObj.append(getProjectIssues(project))
        return projectObj
    except Exception as e:
        traces()
        print(f"Something bad happened: {e}")


def getProjectIssues(project):
    '''Get all the issues in the project and return json object'''
    global base_url, auth, headers
    key = project['key']
    url = f"{base_url}/rest/api/3/search?jql=project={key}&maxResult=1000"
    response = request("GET", url, headers=headers, auth=auth)
    #print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
    return response.json()  # json.loads(response.text)


def getProject(projectkey):
    '''Provides project in json format'''
    global base_url, auth, headers
    url = f"{base_url}/rest/api/3/project/{projectkey}"
    response = request("GET", url, headers=headers, auth=auth)
    project = getProjectIssues(response.json())
    return project


def jsonDump(payload):
    return json.dumps(payload, sort_keys=True, indent=4, separators=(",", ": "))


# for issue in project['issues']:
# print(issue.key)

def progressOfIssues(issues):
    for issue in issues:
        fields = issue['fields']
        print(jsonDump(issues))
        # print(f"issue number= {issue['key']}\nissue summary={fields['summary']}\nprogress={fields['status']['name']}\nAssigned to: {fields['assignee']['displayName'] if fields['assignee'] else fields['assignee']}")
        print()


# progressOfIssues(getProject("SM")['issues'])


def traces():
    global tb_on
    if tb_on:
        tb = traceback.format_exc()
        print(f"traces {tb}")


def get_transitions(key):
    """Get the transitions avaialble for the story"""
    global base_url, auth, headers
    url = f"{base_url}/rest/api/3/issue/{key}/transitions"
    print(url)
    response = request("GET", url, headers=headers, auth=auth)

    return response.json()['transitions']


def manageIssue(key, transitionTo):
    global base_url, headers, auth
    transitions = get_transitions(key)
    print(transitions)
    available_trans = {}
    for transition in transitions:
        available_trans[transition['name']] = transition['id']
    if transitionTo not in available_trans:
        print("Transition is not availble for this issue")
        return
    url = f"{base_url}/rest/api/3/issue/{key}/transitions"

    payload = constructPayload(['move'], available_trans)
    '''json.dumps({
        "transition": {
            "id": available_trans[transitionTo]
        }
    })'''
    response = request("POST", url, data=payload, headers=headers, auth=auth)
    print(response.status_code)


def constructPayload(actions, available_trans):
    payload = {}
    if "move" in actions:
        payload["transition"] = {
            "id": available_trans['In Progress']
        }
    if "comment" in actions:
        payload["update"] = {
            "comment": [
                {
                    "add": {
                        "body": {
                            "content": [
                                {
                                    "content": [
                                        {
                                            "text": "Bug has been fixed",
                                            "type": "text"
                                        }
                                    ],
                                    "type": "paragraph"
                                }
                            ],
                            "type": "doc",
                            "version": 1
                        }
                    }
                }
            ]
        }
    if "assign" in actions:
        payload['fields'] = {
            "asignee": {
                "name": "Hamad"
            }
        }
    return json.dumps(payload)


# manageIssue("SM-2", "Done")

def issueComment(issue):
    global base_url, auth, headers

    url = f"{base_url}/rest/api/3/issue/{issue}/comment"

    print(url)
    response = request(
        "GET",
        url,
        headers=headers,
        auth=auth
    )

    print(jsonDump(response.json()))


def getComments(issues):
    if type(issues) is list:
        for issue in issues:
            issueComment(issue)
    else:
        issueComment(issues)


#getComments(['SM-4', 'SM-2'])


def addComment(issue, comment):
    global base_url, auth, headers

    url = f"{base_url}/rest/api/3/issue/{issue}/comment"

    payload = json.dumps(
        {
            "body": {
                "content": [
                    {
                        "content": [
                            {
                                "attrs": {
                                    "accessLevel": "",
                                    "id": "63d718a4f1475ad42c574c23",
                                    "localId": "dfc57653-e4d1-4272-b449-039114e324ae",
                                    "text": "@Hamad Ullah"
                                },
                                "type": "mention"
                            },
                            {
                                "text": comment,
                                "type": "text"
                            }
                        ],
                        "type": "paragraph"
                    }
                ],
                "type": "doc",
                "version": 1
            }
        })
    response = request(
        "POST",
        url,
        data=payload,
        headers=headers,
        auth=auth
    )
    print(jsonDump(response.json()))

if __name__ == "__main__":
    tb_on = True
    jira_url = "https://viziontech.atlassian.net/rest/api/3/project"

    base_url = "https://viziontech.atlassian.net"

    user_email = ''
    api_token = ''
    readfile = open('.env', 'r').read().split('\n')
    #read .env file save token as <var_name>=<token> and emails as <var_name>=<user_email>
    for line in readfile:
        if 'user_email' in line:
            user_email = line[11:].strip()
        #load token
        elif 'viziontech' in line:
            api_token = line[line.index('=')+1:]
    print(api_token)
        
            

    #api_token = open(".env", 'r').readline().split()[0]  # .split("=")[1].strip().strip('\n')

    auth = HTTPBasicAuth(user_email, api_token)

    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    print(getAllProjects())


#addComment("SM-4", " Just trying to see if this is working 2")

# getAllProjects()
