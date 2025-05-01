import os
import requests
from flask import Flask, request
from requests import Response

app = Flask(__name__)

access_token = os.getenv('GITEA_ACCESS_TOKEN')
org_name = os.getenv('ORGANISATION')
repo_name = os.getenv('REPOSITORY')
git_url = os.getenv('GIT_URL')

def get_payload(line: str) -> list:
    data = line.split('=')[1].strip()
    return data.split(' ') if ' ' in data else [data]

def execute_merge(entry: str) -> Response:
    print('Executing merge for ' + entry)
    url = f"{git_url}/api/v1/repos/{org_name}/{repo_name}/pulls{entry}/merge&token={access_token}"
    params = {
        "Do": "merge",
        "MergeMessageField": "string",
        "MergeTitleField": "string",
        "force_merge": True
    }
    print('Calling ' + f"{git_url}/api/v1/repos/{org_name}/{repo_name}/pulls{entry}/merge&token=********")
    response = requests.post(url, params)
    print('Received response:')
    print(response.text)
    print(response.reason)
    return response



@app.route('/', methods=['GET'])
def get():
    return '', 200


@app.route('/merge', methods=['POST'])
def listen():
    data = request.data.decode('utf-8')
    print('Received payload for merge:')
    print(data)
    if 'text=' not in data:
        return '', 400

    for line in data.split('\n'):
        if 'text=' in line:
            for entry in get_payload(line):
                execute_merge(entry)
        else:
            print('No data found')

    return '', 200

def do_checks():
    message = []

    if git_url is None or '' == git_url.strip():
        message.append('Git url is not set')
    if access_token is None or '' == access_token.strip():
        message.append('No git access token set')
    if org_name is None or '' == org_name.strip():
        message.append('No organisation is set')
    if repo_name is None or '' == repo_name.strip():
        message.append('No repository is set')

    if len(message) > 0:
        for line in message:
            print(line)
        exit()

def sanitize():
    global git_url
    if git_url.endswith('/'):
        git_url = git_url[:-1]

if __name__ == '__main__':
    print('Executing env checks')
    do_checks()
    sanitize()
    app.run(debug=False, port=5000)