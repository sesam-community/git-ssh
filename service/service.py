from flask import Flask, Response, send_from_directory
import json
import os
import logging
from git import Repo
from glob import glob
from pathlib import Path

app = Flask(__name__)

logger = logging.getLogger('service')
working_dir = 'tmp_files'


@app.route('/<path>', defaults={"path": '/'})
def get_entities(path):
    _sync_repo()
    path = "%s/%s" % (working_dir, path)
    files = glob(path)
    if len(files) == 1 and Path(files[0]).is_file():
        return send_from_directory(os.path.abspath(working_dir), path)
    entities = []
    for f in files:
        p = Path(f)
        entities.append({"_id": p.name, "is_dir": p.is_dir(), "is_file": p.is_file()})
    return Response(json.dumps(entities), mimetype='application/json', )


def _sync_repo():
    ssh_cmd = 'ssh -o "StrictHostKeyChecking=no" -i id_deployment_key'
    if not os.path.exists(working_dir):
        repo_url = os.environ['GIT_REPO']
        logger.info('cloning %s', repo_url)
        Repo.clone_from(repo_url, working_dir, env=dict(GIT_SSH_COMMAND=ssh_cmd))
    elif not os.environ.get('SKIP_RESYNC', False):
        repo = Repo(working_dir)
        with repo.git.custom_environment(GIT_SSH_COMMAND=ssh_cmd):
            logger.info('fetching %s origin')
            repo.remotes.origin.fetch()


if __name__ == '__main__':
    with open("id_deployment_key", "w") as key_file:
        key_file.write(os.environ['SSH_PRIVATE_KEY'])
    os.chmod("id_deployment_key", 0o600)

    app.run(debug=True, host='0.0.0.0')
