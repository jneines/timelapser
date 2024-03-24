#!/usr/bin/env python3
from pathlib import Path
import asyncio
import shlex
import datetime as dt
from zoneinfo import ZoneInfo

from loguru import logger

from timelapser.paths import log_dir


class VideoProcessor(object):
    def __init__(self, camera_name, timezone, videos_base_dir):
        self.camera_name = camera_name
        self.timezone = ZoneInfo(timezone)
        self.videos_base_dir = Path(videos_base_dir)

    async def init(self):
        logger.info("Creating ffmpeg task")

        now = dt.datetime.now(self.timezone)
        video_dir = self.videos_base_dir / f"{now:%Y}" / f"{now:%Y%m%d}"
        video_dir.mkdir(exist_ok=True, parents=True)

        available_videos_count = len(
            list(video_dir.glob(f"{self.camera_name}-{now:%Y%m%d}-*.mp4"))
        )
        video_filename = (
            f"{self.camera_name}-{now:%Y%m%d}-{available_videos_count+1:03d}.mp4"
        )
        # make a subdirectory structure below video_path, which is tree like to optimize
        # fs access times
        video_path = video_dir / video_filename

        # ENV='FFREPORT=file="./%p-%t.log":level=32'
        ffmpeg_log_file = (log_dir / "%p-%t.log").as_posix()
        cmd = (
            "/usr/bin/ffmpeg -y "
            "-hide_banner "
            "-report "
            "-nostats "
            "-f image2pipe -i pipe:0 "
            "-f lavfi -i anullsrc -c:a aac "
            "-filter:v scale=1280:720 "
            "-b:v 2M -c:v h264 -profile:v high422 "
            "-shortest "
            f"{video_path}"
        )
        logger.info(f"Using ffmpeg like this: {cmd}.")

        args = shlex.split(cmd)
        try:
            self.ffmpeg = await asyncio.subprocess.create_subprocess_exec(
                *args,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL,
                env={"FFREPORT": f"file={ffmpeg_log_file}:level=32"},
            )

        except (FileNotFoundError,) as e:
            # asyncio.subprocess.SubprocessError) as e:
            logger.error(f"Error starting the video processor. Error message was {e}")

    async def feed(self, image):
        logger.debug("Feeding new image to ffmpeg")
        self.ffmpeg.stdin.write(image)
        await self.ffmpeg.stdin.drain()

    async def close(self):
        # close ffmpeg task
        if self.ffmpeg:
            logger.info("Finalizing ffmpeg video")
            await self.ffmpeg.stdin.drain()
            self.ffmpeg.stdin.close()
            await self.ffmpeg.wait()
