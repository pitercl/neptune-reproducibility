import subprocess
import neptune
import sys
import os

project = neptune.init()

exp_name = sys.argv[1]

exps = project.get_experiments(exp_name)

exp = exps[0]

props = exp.get_properties()

cmd = props["cmd"]
docker_image = props["docker_image"]
docker_extra_params = props["docker_extra_params"]

git_remote = props["git_remote"]
git_sha = props["git_sha"]

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
              "-e", "DOCKER_EXTRA_PARAMS=" + docker_extra_params
          ] + docker_extra_params.split(" ") + [
              docker_image,
              "-c",
              "&& pip install neptune-client && git clone -q \"$GIT_REPO\" /repo && cd /repo && git checkout -q \"$GIT_COMMIT_SHA\" && $RUN_COMMAND"
          ]

subprocess.Popen(command, shell=False).communicate()
