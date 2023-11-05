#!/usr/bin/env python3
from pathlib import Path

from platformdirs import user_config_dir, user_log_dir, user_data_dir

config_dir = Path(user_config_dir("timelapser"))
data_dir = Path(user_data_dir("timelapser"))
log_dir = Path(user_log_dir("timelapser"))

program_dir = data_dir / "programs"
videos_base_dir = data_dir / "videos"
photos_base_dir = data_dir / "photos"


# make sure all directories actually exist
for _dir in (config_dir, data_dir, log_dir, program_dir, videos_base_dir, photos_base_dir):
    _dir.mkdir(exist_ok=True, parents=True)
