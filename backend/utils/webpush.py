import logging

logger = logging.getLogger(__name__)

def wp_send_message(devices, message):
    for device in devices:
        try:
            device.send_message(message)
        except Exception as e:
            device.delete()
            logger.exception(e)
