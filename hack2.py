
import git
import subprocess
import neptune
import sys

git_repo = git.Repo('.', search_parent_directories=True)
git_root = git_repo.git.rev_parse("--show-toplevel")

path = git_root + "/repro.yaml"

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

command = "docker run -it --entrypoint '/bin/bash' -v ~/.ssh:/root/.ssh:ro " \
          + " -e NEPTUNE_PROJECT=" + project.full_id \
          + " -e NEPTUNE_API_TOKEN=" + os.getenv("NEPTUNE_API_TOKEN", "") \
          + " -e RUN_COMMAND=\"" + cmd + "\"" \
          + " -e GIT_REPO=\"" + git_remote + "\"" \
          + " -e GIT_COMMIT_SHA=" + git_sha \
          + " -e DOCKER_IMAGE=" + docker_image \
          + " -e DOCKER_EXTRA_PARAMS=\"\"" + docker_extra_params \
          + " " + docker_extra_params + docker_image \
          + " -c 'git clone \"$GIT_REPO\" /repo && cd /repo && git checkout \"$GIT_COMMIT_SHA\" && echo $RUN_COMMAND'"

subprocess.run(command, shell=True, check=True)
