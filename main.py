import os
import neptune

neptune.init()

# We're now creating the most basic experiment
with neptune.create_experiment("My Experiment") as exp:

    # First, we save information required for reproducibility
    exp.set_property("git_remote", os.getenv("GIT_REPO", ""))
    exp.set_property("docker_image", os.getenv("DOCKER_IMAGE", ""))
    exp.set_property("docker_extra_params", os.getenv("DOCKER_EXTRA_PARAMS", ""))
    exp.set_property("cmd", os.getenv("RUN_COMMAND", ""))
    exp.set_property("git_sha", os.getenv("GIT_COMMIT_SHA", ""))

    # We can now proceed with our experiment, track metrics, artifacts, etc
    # ...
    pass
