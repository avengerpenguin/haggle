import asyncio
from typing import Callable

import aiohttp
import aiohttp_jinja2
import functools
from accept_types import get_best_match
from aiohttp import web
from aiohttp.web_response import Response


def negotiate(template: str) -> Callable:
    """
    Wraps a request handler in order to render the given template if the client
    is a browser but also return the template context as JSON if the requester
    sets Accept: application/json.

    The idea here is that a handler need only return a normal dict object and
    then you can annotate that handler with this decorator to magically decide
    between returning the data as JSON or returning HTML by passing the same
    data to the named template.

    :param template: The template to render if HTML is requested.
    :return: A decorator for rewrapping a request handler.
    """

    def wrapper(func: Callable) -> Callable[[], Response]:

        @asyncio.coroutine
        @functools.wraps(func)
        def wrapped(*args) -> Response:

            if asyncio.iscoroutinefunction(func):
                coro = func
            else:
                coro = asyncio.coroutine(func)
            output = yield from coro(*args)

            if isinstance(output, web.StreamResponse):
                return output

            request = args[-1]

            header = request.headers.get('Accept', '*/*')

            return_type = get_best_match(
                header,
                ['text/html', 'application/json'])

            if return_type == 'application/json':
                response = aiohttp.web.json_response(output)
                response.headers['Access-Control-Allow-Origin'] = '*'
                return response
            else:
                response = aiohttp_jinja2.render_template(
                    template,
                    request,
                    output
                )
                response.headers['Access-Control-Allow-Origin'] = '*'
                return response

        return wrapped

    return wrapper
