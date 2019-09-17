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
    async def async_handler(_request):
        return {'head': 'HEAD', 'text': 'text'}

    # Create a non-async handler too to prove we can support either
    @negotiate('example.template')
    def sync_handler(_request):
        return {'head': 'HEAD', 'text': 'text'}

    @negotiate('example.template')
    def normal_handler(_request):
        return web.Response(text='Hello, world!')


    # Create real app using stub handler and return a test client for it
    app.router.add_route('*', '/async', async_handler)
    app.router.add_route('*', '/sync', sync_handler)
    app.router.add_route('*', '/normal', normal_handler)

    return await aiohttp_client(app)


async def test_omitting_accept_header_renders_html_async(client):
    resp = await client.get('/async')
    assert 200 == resp.status
    txt = await resp.text()
    assert '<html><body><h1>HEAD</h1>text</body></html>' == txt


async def test_html_accept_header_renders_html_async(client):
    resp = await client.get('/async', headers={'Accept': 'text/html'})
    assert 200 == resp.status
    txt = await resp.text()
    assert '<html><body><h1>HEAD</h1>text</body></html>' == txt


async def test_json_accept_header_renders_json_async(client):
    resp = await client.get('/async', headers={'Accept': 'application/json'})
    assert 200 == resp.status
    response_json = await resp.json()
    assert {'head': 'HEAD', 'text': 'text'} == response_json


async def test_omitting_accept_header_renders_html_sync(client):
    resp = await client.get('/sync')
    assert 200 == resp.status
    txt = await resp.text()
    assert '<html><body><h1>HEAD</h1>text</body></html>' == txt


async def test_html_accept_header_renders_html_sync(client):
    resp = await client.get('/sync', headers={'Accept': 'text/html'})
    assert 200 == resp.status
    txt = await resp.text()
    assert '<html><body><h1>HEAD</h1>text</body></html>' == txt


async def test_json_accept_header_renders_json_sync(client):
    resp = await client.get('/sync', headers={'Accept': 'application/json'})
    assert 200 == resp.status
    response_json = await resp.json()
    assert {'head': 'HEAD', 'text': 'text'} == response_json


async def test_handlers_returning_a_response_are_untouched(client):
    resp = await client.get('/normal')
    assert 200 == resp.status
    txt = await resp.text()
    assert 'Hello, world!' == txt
