import logging
from collections.abc import Awaitable, Callable

from datacommons_client import use_api_key
from starlette.datastructures import MutableHeaders
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger(__name__)


class APIKeyMiddleware(BaseHTTPMiddleware):
    """
    Middleware to extract X-API-Key header and set it as the override API key
    for the Data Commons client context.
    """

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        api_key = request.headers.get("X-API-Key")
        if api_key:
            logger.debug("Received X-API-Key header, applying override.")
            try:
                with use_api_key(api_key):
                    return await call_next(request)
            except Exception as e:
                # We log and re-raise to ensure we don't swallow application errors,
                # but we want to know if the context manager itself failed.
                logger.error("Error during API key override context propagation: %s", e)
                raise
        else:
            return await call_next(request)


class AcceptMiddleware(BaseHTTPMiddleware):
    """
    Middleware to ensure the Accept header is compatible with MCP (SSE) and JSON-RPC.
    It rewrites 'Accept: */*' or missing Accept headers to 'text/event-stream, application/json'.
    """

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        accept_header = request.headers.get("Accept", "")
        logger.info("Received Accept header: %s", accept_header)
        return await call_next(request)
        # Apply strict MCP requirements if client is being generic (*/*) or missing header
        if "*/*" in accept_header or not accept_header:
            logger.debug(
                "Rewriting Accept header from '%s' to 'text/event-stream, application/json'",
                accept_header,
            )
            headers = MutableHeaders(scope=request.scope)
            headers["Accept"] = "text/event-stream, application/json"

            # Clear Starlette's cached headers to ensure call_next sees the update
            if hasattr(request, "_headers"):
                del request._headers

        return await call_next(request)
