from typing import Callable

import aiohttp_jinja2
import jinja2
import pytest
from aiohttp import web
from aiohttp.test_utils import TestClient
from aiohttp_jinja2_haggle import negotiate


@pytest.fixture
async def client(aiohttp_client) -> TestClient:

    # Tell jinja2 to load a fixture template rather than read the disk
    template = '<html><body><h1>{{head}}</h1>{{text}}</body></html>'
    app = web.Application()
    aiohttp_jinja2.setup(app, loader=jinja2.DictLoader({
        'example.template': template
    }))

    # Create request handler that uses fixture template when HTML is requested
    @negotiate('example.template')
    async def my_handler(_request):
        return {'head': 'HEAD', 'text': 'text'}

    # Create real app using stub handler and return a test client for it
    app.router.add_route('*', '/', my_handler)
    return await aiohttp_client(app)


async def test_omitting_accept_header_renders_html(client):
    resp = await client.get('/')
    assert 200 == resp.status
    txt = await resp.text()
    assert '<html><body><h1>HEAD</h1>text</body></html>' == txt


async def test_html_accept_header_renders_html(client):
    resp = await client.get('/', headers={'Accept': 'text/html'})
    assert 200 == resp.status
    txt = await resp.text()
    assert '<html><body><h1>HEAD</h1>text</body></html>' == txt


async def test_json_accept_header_renders_json(client):
    resp = await client.get('/', headers={'Accept': 'application/json'})
    assert 200 == resp.status
    response_json = await resp.json()
    assert {'head': 'HEAD', 'text': 'text'} == response_json
