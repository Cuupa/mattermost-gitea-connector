import os
import requests
from flask import Flask, request

app = Flask(__name__)

access_token = os.getenv('GITEA_ACCESS_TOKEN')
org_name = os.getenv('ORGANISATION')
repo_name = os.getenv('REPOSITORY')
git_url = os.getenv('GIT_URL')

def get_payload(line: str) -> list:
    data = line.split('=')[1].strip()
    return data.split(' ') if ' ' in data else [data]

def execute_merge(entry: str):
    url = f"{git_url}/api/v1/repos/{org_name}/{repo_name}/pulls{entry}/merge&token={access_token}"
    params = {
        "Do": "merge",
        "MergeMessageField": "string",
        "MergeTitleField": "string",
        "force_merge": True
    }
    requests.post(url, params)


@app.route('/', methods=['GET'])
def get():
    return '', 200


@app.route('/', methods=['POST'])
def listen():
    data = request.data.decode('utf-8')

    if 'text=' not in data:
        return '', 400

    lines = data.split('\n')
    for line in lines:
        if 'text=' in line:
            payload = get_payload(line)
            for entry in payload:
                execute_merge(entry)

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

if __name__ == '__main__':
    do_checks()
    app.run(debug=False, port=5000)