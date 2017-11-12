from picamera import PiCamera
import logging
import subprocess
from logging.config import fileConfig
from log import setup_custom_logger
logger = logging.getLogger(__name__)  


class CameraControl(object):
    def __init__(self):
        logger = setup_custom_logger(__name__)
        logger.debug('Starting %s', 'CameraControl')

    def takeSingle(self,currentDateTime):
        logger.debug('starting takeSingle')
        try:
            try:
                c = subprocess.check_output(["vcgencmd","get_camera"])
                int(camdet.strip()[-1]) #-- Removes the final CR character and gets only the "0" or "1" from detected status
                if (c):
                    logger.debug( "Camera detected")
                    camera = PiCamera()
                    camera.start_preview()
                    camera.capture('image' + currentDateTime.strftime('%Y%m%d%H%M%-S') + '.jpg')
                    camera.stop_preview()
                    camera.close()
                    logger.debug('taken picture')
                else:
                    logger.warn( "not detected")
            except Exception as ex:
                logger.warn(format(ex))
        except SystemExit as e:
            if e.code != EMERGENCY:
                logger.error(format(e))
            else:
                os._exit(EMERGENCY)  # try to stop *that*, sucker!