import os
import neptune

neptune.init()

experiment = neptune.create_experiment("Repro v2")

experiment.set_property("git_remote", os.getenv("GIT_REPO", ""))
experiment.set_property("docker_image", os.getenv("DOCKER_IMAGE", ""))
experiment.set_property("docker_extra_params", os.getenv("DOCKER_EXTRA_PARAMS", ""))
experiment.set_property("cmd", os.getenv("RUN_COMMAND", ""))
experiment.set_property("git_sha", os.getenv("GIT_COMMIT_SHA", ""))

neptune.stop()
