"""Main module."""
import sys
import asyncio
import time
import datetime as dt
from zoneinfo import ZoneInfo
import io

from PIL import Image
from loguru import logger

from timelapser.paths import photos_base_dir


class TimeLapser(object):
    BEFORE_START=2
    EXECUTING=1
    COMPLETE=0

    def __init__(self, camera, video_processor, program):
        self.camera = camera
        self.video_processor = video_processor
        self.timezone = ZoneInfo(program["timezone"])
        self.start_ts = program["start_ts"]
        self.end_ts = program["end_ts"]
        self.shoot_every = program["every"]

        self.idle_time = 1
        self.keep_running = True
        self.return_code = TimeLapser.BEFORE_START

    async def shoot(self):
        now = dt.datetime.now(self.timezone)
        logger.debug(f"Starting to shoot at {now}")

        logger.debug(f"{self.start_ts=}")
        logger.debug(f"{self.end_ts=}")
        logger.debug(f"{self.shoot_every=}")

        # camera and day specific photos dir
        photos_dir = photos_base_dir / self.camera.name / f"{now:%Y%m%d}"
        photos_dir.mkdir(exist_ok=True, parents=True)
        logger.debug(
            f"Using {photos_dir.as_posix()} to save photos for this program."
        )

        wait_for_start = max(0, (self.start_ts - now).total_seconds())
        logger.info(f"Waiting for {wait_for_start} seconds, before starting to shoot.")
        await asyncio.sleep(wait_for_start)

        self.return_code = TimeLapser.EXECUTING

        image_count = 0
        while self.keep_running:
            now = dt.datetime.now(self.timezone)
            if now > self.end_ts:
                self.keep_running = False
                self.return_code = TimeLapser.COMPLETE
                continue
            

            tic = time.time()
            image = self.camera.get_image()
            if image:
                # TODO: do we really need an updated timestamp here?
                now = dt.datetime.now(self.timezone)
                # TODO: Add the crop feature here before saving and feeding the image
                # TODO: make this a camera_name dependent storage to allow more cameras to be used
                with (photos_dir / f"{now:%Y%m%d-%H%M%S}.jpg").open("wb") as fd:
                    fd.write(image)
                im = Image.open(io.BytesIO(image))
                # log image size (geometry)
                logger.debug(f"Image size: {im.size}")
                image_count += 1
                await self.video_processor.feed(image)
                # log image size (bytes)
                image_size = len(image)
                logger.info(
                    f"Shot image #{image_count} with size {image_size:_d} bytes."
                )
            toc = time.time()
            idle_for = max(0, self.shoot_every - (toc - tic))
            await asyncio.sleep(idle_for)

    async def run(self):
        await self.video_processor.init()
        self.shooting_task = asyncio.create_task(self.shoot())
        while self.keep_running:
            await asyncio.sleep(self.idle_time)

        await self.video_processor.close()
        sys.exit(self.return_code)


    def exit(self, *args):
        self.keep_running = False
