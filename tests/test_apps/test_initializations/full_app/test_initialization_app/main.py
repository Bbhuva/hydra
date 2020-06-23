# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import os
import sys

from hydra.experimental import (
    compose,
    initialize_config_dir_ctx,
    initialize_config_module_ctx,
    initialize_ctx,
)


# TODO: move all nox tested standalone apps into tests/standalone_apps
def main() -> None:
    with initialize_ctx(config_path="conf"):
        cfg = compose(config_name="config", return_hydra_config=True)
        assert cfg.config == {"hello": "world"}
        assert cfg.hydra.job.name == "app"

    with initialize_ctx(config_path="conf", job_name="test_job"):
        cfg = compose(config_name="config", return_hydra_config=True)
        assert cfg.config == {"hello": "world"}
        assert cfg.hydra.job.name == "test_job"

    abs_config_dir = os.path.abspath("test_initialization_app/conf")
    with initialize_config_dir_ctx(config_dir=abs_config_dir):
        cfg = compose(config_name="config", return_hydra_config=True)
        assert cfg.config == {"hello": "world"}
        assert cfg.hydra.job.name == "app"

    with initialize_config_dir_ctx(config_dir=abs_config_dir, job_name="test_job"):
        cfg = compose(config_name="config", return_hydra_config=True)
        assert cfg.config == {"hello": "world"}
        assert cfg.hydra.job.name == "test_job"

    # Those tests can only work if the module is installed
    if len(sys.argv) > 1 and sys.argv[1] == "module_installed":
        with initialize_config_module_ctx(config_module="test_initialization_app.conf"):
            cfg = compose(config_name="config", return_hydra_config=True)
            assert cfg.config == {"hello": "world"}
            assert cfg.hydra.job.name == "app"

        with initialize_config_module_ctx(
            config_module="test_initialization_app.conf", job_name="test_job"
        ):
            cfg = compose(config_name="config", return_hydra_config=True)
            assert cfg.config == {"hello": "world"}
            assert cfg.hydra.job.name == "test_job"


if __name__ == "__main__":
    main()
