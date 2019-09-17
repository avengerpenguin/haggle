# Haggle: HTTP Negotiation for humans and machines alike

[![Build Status](https://travis-ci.org/avengerpenguin/haggle.svg?branch=master)](https://travis-ci.org/avengerpenguin/haggle)

Helper libraries for automatically making Python services render both an HTML and a
machine-readable view for any endpoint.

The idea is to build handler functions that simply return `dict`-like objects of data and
a `negotiate` wrapper decides whether to render that `dict` as JSON or set it as the
context for a template render.

The main use case allows for you to build quick HTML views of data
(reports, dashboards, etc.) that are automatically consumable by other systems with no
additional effort. You merely use the haggle `negotiate` wrapper instead of a template
decorator you are already using.

Currently only supports aiohttp and jinja2. To install

```
$ pip install aiohttp-jinja2-haggle
```

Then to use:

```python
from aiohttp_jinja2_haggle import negotiate


@negotiate('example_template.html')
async def async_handler(_request):
    return {'foo': 'bar'}
```

This will return the dict `{'foo': 'bar'}` as JSON if and only if the request has
the `Accept` header set to `application/json`.
If not, this will instead render `example_template.html`
(via [aiohttp_jinja2](https://github.com/aio-libs/aiohttp-jinja2)) with the dict
`{'foo': 'bar'}` as the template context