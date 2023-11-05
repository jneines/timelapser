#!/usr/bin/env python3
import json

from timelapser.paths import config_dir, videos_base_dir


def read_config(config_name):
    # default config with sane entries
    config = {
            "videos_base_dir": videos_base_dir,
            }

    # read specified config file
    with (config_dir / f"{config_name}.json").open("r") as fd:
        _config = json.loads(fd.read())

    config.update(_config)

    return config
