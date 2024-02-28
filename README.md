# [Odesli](https://odesli.co) API Wrapper

[![Python 3.11](https://img.shields.io/badge/python-^3.11-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](https://mit-license.org/)

A fast and asynchronous wrapper for the Odesli (song.link, album.link) written in Python

API Documentation: [notion.site](https://linktree.notion.site/API-d0ebe08a5e304a55928405eb682f6741)

## Installation

```bash
pip3 install git+https://github.com/ulbwa/odesli_api_python
```
or
```bash
poetry add git+https://github.com/ulbwa/odesli_api_python
```

## Usage example

```python
import asyncio

from odesli_api import Odesli

odesli = Odesli()


async def main():
    links = await odesli.links_by_url("https://open.spotify.com/album/5Z9iiGl2FcIfa3BMiv6OIw?si=6Vb9yJiKSM6C0lpyfPZbfQ")
    print(links)

asyncio.run(main())
```

