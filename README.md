## Reproducing experiments in Neptune [quick & dirty POC]

The most basic way to reproduce experiments with Neptune.

### How to run

```py

pip install GitPython PyYAML neptune-client

export NEPTUNE_PROJECT=<my username/my project>
export NEPTUNE_API_TOKEN=<my API Token>


python3 ./neptune_run.py


python3 ./neptune_rerun.py <experiment id, e.g. SAN-123>

```
