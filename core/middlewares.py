import json
import logging

from django.utils.timezone import now


class LoggingMiddleware:
    """
    Middleware that logs request and response details for debugging and auditing.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger("django.request")
        self.logger.setLevel(logging.DEBUG)

    def __call__(self, request):
        """Logs request and response details."""
        self.log_request(request)
        response = self.get_response(request)
        self.log_response(request, response)
        return response

    def log_request(self, request):
        """Logs incoming requests."""
        self.logger.info(
            f"Incoming Request: {request.method} {request.path} | "
            f"IP: {request.META.get('REMOTE_ADDR')} | Time: {now()}"
        )

    def log_response(self, request, response):
        """Logs outgoing responses and errors."""
        log_message = (
            f"Response: {response.status_code} | "
            f"Time: {now()} | Request: {request.method} {request.path}"
        )

        if response.status_code >= 400:
            try:
                response_content = response.content.decode("utf-8")
                if "application/json" in response.get("Content-Type", ""):
                    response_content = json.dumps(json.loads(response_content), indent=2)
            except (UnicodeDecodeError, json.JSONDecodeError):
                response_content = "[Unable to decode response content]"

            self.logger.error(f"{log_message} | Details: {response_content}")
        else:
            self.logger.info(log_message)

    def process_exception(self, request, exception):
        """Logs unhandled exceptions."""
        self.logger.error(
            f"Exception occurred: {exception} | Time: {now()} | "
            f"Request: {request.method} {request.path}",
            exc_info=True
        )
