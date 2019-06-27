
import yaml
import git
import subprocess
import neptune
import os

git_repo = git.Repo('.', search_parent_directories=True)
git_root = git_repo.git.rev_parse("--show-toplevel")

path = git_root + "/repro.yaml"

project = neptune.init()

with open(path) as stream:
    data = yaml.safe_load(stream)
    cmd = data["cmd"]
    docker_image = data["docker"]["image"]
    docker_extra_params = data["docker"]["params"]

    git_remote =  git_repo.remote().url
    git_sha = git_repo.head.commit.hexsha

    command = [
        "docker", "run", "-it",
        "--entrypoint", "/bin/bash",
        "-v", os.path.expanduser("~") + "/.ssh:/root/.ssh:ro",
        "-e", "NEPTUNE_PROJECT=" + project.full_id,
        "-e", "NEPTUNE_API_TOKEN=" + os.getenv("NEPTUNE_API_TOKEN", ""),
        "-e", "RUN_COMMAND=" + cmd + "",
        "-e", "GIT_REPO=" + git_remote + "",
        "-e", "GIT_COMMIT_SHA=" + git_sha,
        "-e", "DOCKER_IMAGE=" + docker_image + "",
        "-e", "DOCKER_EXTRA_PARAMS=" + docker_extra_params,
        docker_image,
        "-c", "git clone -q \"$GIT_REPO\" /repo && cd /repo && git checkout -q \"$GIT_COMMIT_SHA\" && $RUN_COMMAND"
    ]

    subprocess.Popen(command, shell=False).communicate()
    # subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE)
