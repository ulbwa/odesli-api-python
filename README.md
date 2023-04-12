# [SongLink](https://odesli.co) API Wrapper

[![Python 3.10](https://img.shields.io/badge/python-^3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](https://mit-license.org/)

A fast and asynchronous wrapper for the SongLink API written in Python.

API Documentation: [notion.site](https://linktree.notion.site/API-d0ebe08a5e304a55928405eb682f6741)

## Installation

```bash
pip3 install git+https://github.com/ulbwa/SongLinkAPI
```
or
```bash
poetry add git+https://github.com/ulbwa/SongLinkAPI
```

## Usage example

```python
import asyncio

from SongLinkAPI import SongLink

songlink = SongLink()


async def main():
    links = await songlink.links_by_url("https://open.spotify.com/album/5Z9iiGl2FcIfa3BMiv6OIw?si=6Vb9yJiKSM6C0lpyfPZbfQ")
    print(links)

asyncio.run(main())
```

