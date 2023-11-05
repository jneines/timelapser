#!/usr/bin/env python3
import platform
import requests

from loguru import logger


class IPCamera(object):
    def __init__(self, name, snapshot_url, max_attempts=5):
        self.name = name
        self.snapshot_url = snapshot_url
        self.max_attempts = max_attempts

    def get_image(self):
        for attempt_index in range(self.max_attempts):
            try:
                r = requests.get(self.snapshot_url, stream=True)
                if r.status_code == 200:
                    return r.content
                else:
                    logger.warning(
                        f"Problems occured fetching the image at attempt #{attempt_index+1}/{self.max_attempts+1}. Retrying ..."
                    )
            except requests.exceptions.ConnectionError as e:
                logger.error(e)
        logger.error(
            f"Unable to fetch image after {self.max_attempts+1} attempts. Giving up."
        )


if __name__ == "__main__":
    import sys
    import signal

    camera_name = "picamera1"

    camera = IPCamera(camera_name, f"http://{camera_name}:8080/snapshot")
    image = camera.get_image()
    logger.debug(f"Test image size is {len(image):_d} bytes.")
