"""Console script for timelapser."""
import sys
import click
import asyncio
import signal

from loguru import logger

from timelapser.config import read_config
from timelapser.program import load_program
from timelapser.ip_camera import IPCamera
from timelapser.video_processor import VideoProcessor
from timelapser.timelapser import TimeLapser


@click.command()
@click.option("-c", "--config-name", type=str, required=True, help="Config name to use")
def main(config_name):
    logger.debug(f"Using {config_name=}.")

    config = read_config(config_name)
    logger.debug(config)

    program = load_program(config["program"])
    logger.debug(program)

    camera_name = config["camera_name"]
    snapshot_url = config["snapshot_url"]
    logger.debug(f"{camera_name=}, {snapshot_url=}")
    camera = IPCamera(camera_name, snapshot_url)
    logger.debug(f"Test image size is {len(camera.get_image()):_d} bytes.")

    timezone = program["timezone"]
    videos_base_dir = config["videos_base_dir"]
    video_processor = VideoProcessor(camera_name, timezone, videos_base_dir)

    tl = TimeLapser(camera, video_processor, program)
    signal.signal(signal.SIGINT, tl.exit)
    asyncio.run(tl.run(), debug=True)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
