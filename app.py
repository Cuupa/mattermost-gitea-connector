import sys
import os
import json
import requests
import logging
from flask import Flask, request
from requests import Response

app = Flask(__name__)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

access_token = os.getenv('GITEA_ACCESS_TOKEN')
org_name = os.getenv('ORGANISATION')
repo_name = os.getenv('REPOSITORY')
git_url = os.getenv('GIT_URL')


def get_payload(data: str) -> list:
    return data.split(' ') if ' ' in data else [data]


def execute_merge(entry: str, user: str) -> Response:
    logger.info('Executing merge for ' + entry)
    url = f"{git_url}/api/v1/repos/{org_name}/{repo_name}/pulls/{entry}/merge?token={access_token}"
    data = {
        "Do": "merge",
        "MergeMessageField": f"Merged by {user} via mattermost",
        "MergeTitleField": "Merged pull request",
        "force_merge": True
    }
    headers = {'Content-Type': 'application/json', 'accept': 'application/json'}
    logger.info('Calling ' + f"{git_url}/api/v1/repos/{org_name}/{repo_name}/pulls{entry}/merge&token=********")
    response = requests.post(url, data=json.dumps(data), headers=headers)
    logger.info('Received response:')
    logger.info(response.text)
    logger.info(response.reason)
    return response


@app.route('/', methods=['GET'])
def get():
    return '', 200


@app.route('/merge', methods=['POST'])
def listen():
    data = request.form
    logger.info('Received payload for merge:')
    logger.info(data)
    if 'text' not in data:
        return '', 400

    for entry in get_payload(data.get('text')):
        execute_merge(entry, data.get('user_name'))

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
            logger.info(line)
        exit()


def sanitize():
    global git_url
    if git_url.endswith('/'):
        git_url = git_url[:-1]


if __name__ == '__main__':
    logger.info('Executing env checks')
    do_checks()
    sanitize()
    app.run(host='0.0.0.0')
