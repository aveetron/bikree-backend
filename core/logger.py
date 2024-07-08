import os
import threading
from datetime import datetime
from enum import Enum

from discord_logger import DiscordLogger
from dotenv import load_dotenv
from requests import Response

from core.http_utils import HttpUtil

load_dotenv()


class LoggerInfo(Enum):
    application_name = "Bikree"
    service_name = "Backend Bot"
    service_environment = "Dev"


options = {
    # Application name would replace the webhook name set during creating of the webhook
    # It would appear as the name of the bot
    # If unset, the default value would be "Application"
    "application_name": LoggerInfo.application_name.value,
    # Service name would be the name of the service sending the message to your Discord channel
    # This would usually be the name of the application sending the notification
    # If unset, the default value would be "Status Bot"
    "service_name": LoggerInfo.service_name.value,
    # Service icon URL is the icon image for your application
    # This field accepts a URL to the icon image
    # If unspecified, the icon wouldn't be set
    # If misconfigured, the icon wouldn't load and a blank space would appear before the service name
    # "service_icon_url": "your icon url",
    # Usually services would run in staging and production environments
    # This field is to specify the environment from which the application is reponding for easy identification
    # If unset, this block would not appear in the message
    "service_environment": LoggerInfo.service_environment.value,
    # An option to specify whether or not to display the hostname in the messages
    # The hostname is set by default, but it could be disabled by specifically setting this to `False`
    "display_hostname": True,
    # The default importance level of the message
    # The left bar color of the message would change depending on this
    # Available options are
    # - default: 2040357
    # - error: 14362664
    # - warn: 16497928
    # - info: 2196944
    # - verbose: 6559689
    # - debug: 2196944
    # - success: 2210373
    # If the `error` field is set during the construction of the message, the `level` is automatically set to `error`
    # If nothing is specified, `default` color would be used
    "default_level": "error",
}


class Logger:

    def __init__(self):
        pass

    @staticmethod
    def discord_logger(e: Exception) -> Response:
        try:
            webhook_url = os.environ.get("webhook_url")
            if not webhook_url:
                raise ValueError("Webhook URL not found in environment variables")

            discord_logger = DiscordLogger(webhook_url=webhook_url, **options)
            discord_logger.construct(
                title=type(e).__name__,
                description=str(e.args[0]) if e.args else "No description",
                metadata={
                    "filename": e.__traceback__.tb_frame.f_code.co_filename,
                    "funcName": e.__traceback__.tb_frame.f_code.co_name,
                    "levelname": "ERROR",
                    "lineno": e.__traceback__.tb_lineno,
                    "module": __name__,
                    # "name": logger.name,
                    "pathname": e.__traceback__.tb_frame.f_code.co_filename,
                    "process": os.getpid(),
                    "processName": "MainProcess",
                    "stack_info": None,
                    "thread": threading.get_ident(),
                    "threadName": threading.current_thread().name,
                    "message": str(e),
                    "time": datetime.now().isoformat(),
                },
            )

            try:
                response = discord_logger.send()
                return response
            except Exception as excep:
                return HttpUtil.error_response(
                    message=f"Failed to send log: {str(excep)}"
                )

        except Exception as err:
            return HttpUtil.error_response(message=f"Logger setup failed: {str(err)}")
