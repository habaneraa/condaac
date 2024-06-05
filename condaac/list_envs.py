"""List all conda environments of the current user."""
# This utility can find all conda environments of the current Linux user
# The logic is copied from the source code of conda:
# https://github.com/conda/conda/blob/main/conda/core/envs_manager.py

import os
from errno import ENOENT

from natsort import natsorted

PREFIX_MAGIC_FILE = os.path.join("conda-meta", "history")


def is_conda_environment(prefix):
    return os.path.isfile(os.path.join(prefix, PREFIX_MAGIC_FILE))


def get_user_environments_txt_file():
    return os.path.expanduser(os.path.join("~", ".conda", "environments.txt"))


def yield_lines(path):
    try:
        with open(path) as fh:
            for line in fh:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                yield line
    except OSError as e:
        if e.errno == ENOENT:
            pass
        else:
            raise


def _clean_environments_txt(environments_txt_file):
    if not os.path.isfile(environments_txt_file):
        return ()

    environments_txt_lines = tuple(yield_lines(environments_txt_file))
    return tuple(
        prefix
        for prefix in environments_txt_lines
        if is_conda_environment(prefix)
    )


def list_env_paths(conda_info_dict):
    all_env_paths = set()

    # look ~/.conda/environments.txt
    environments_txt_file = get_user_environments_txt_file()
    if os.path.isfile(environments_txt_file):
        try:
            all_env_paths.update(_clean_environments_txt(environments_txt_file))
        except PermissionError:
            pass
    
    # look all `env_dirs`
    envs_dirs = (envs_dir for envs_dir in conda_info_dict['envs_dirs'] if os.path.isdir(envs_dir))
    all_env_paths.update(
        env_path
        for env_path in (entry.path for envs_dir in envs_dirs for entry in os.scandir(envs_dir))
        if env_path not in all_env_paths and is_conda_environment(env_path)
    )

    if conda_info_dict['root_prefix'] in all_env_paths:
        all_env_paths.remove(conda_info_dict['root_prefix'])

    return [conda_info_dict['root_prefix']] + natsorted(all_env_paths)
