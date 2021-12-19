import socket
import time
import json
import logging

from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse



#Black-Listde olan userin blocklanmasi

class IPAddressMiddleware(MiddlewareMixin):
    def process_request(self, request):
        print(socket.gethostbyname(socket.gethostname()))

    def process_response(self, request, response):
        BLOCKED_IP = ['127.0.0.5']
        if socket.gethostbyname(socket.gethostname()) in BLOCKED_IP:
            return render(request, "error-404.html")
        return response

"""
Middleware to log `*/api/*` requests and responses.
"""


logging.basicConfig(
    level=logging.DEBUG,
    datefmt="%y-%m-%d %H:%M:%S",
    filename=settings.LOGS_ROOT,
)
logging.getLogger().addHandler(logging.StreamHandler())
logger = logging.getLogger(__name__)

class RequestLogMiddleware:
    """Request Logging Middleware."""

    def __init__(self, get_response):
        self.get_response = get_response
        # print(f'get_ response: {get_response}')

    def __call__(self, request):
        start_time = time.time()
        log_data = {
            "remote_address": request.META["REMOTE_ADDR"],
            "server_hostname": socket.gethostname(),
            "request_method": request.method,
            "request_path": request.get_full_path(),
        }

        # Only logging "*/api/*" patterns
        if "/api/" in str(request.get_full_path()):
            req_body = request.body if request.body else {}
            log_data["request_body"] = req_body

        # request passes on to controller
        response = self.get_response(request)
        print(type(response))
        # add runtime to our log_data
        if response and response["content-type"] == "application/json":
            response_body = json.loads(response.content.decode("utf-8"))
            log_data["response_body"] = response_body
        log_data["run_time"] = time.time() - start_time

        logger.info(msg=log_data)

        return response

    # Log unhandled exceptions as well
    def process_exception(self, request, exception):
        try:
            raise exception
        except Exception as e:
            logger.exception("Unhandled Exception: " + str(e))
        return exception