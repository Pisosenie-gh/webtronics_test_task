import unittest
import asyncio
import aiohttp
from unittest.mock import MagicMock


class TestLogs(unittest.TestCase):
    async def test_logs(self):
        session = MagicMock()
        response = MagicMock()
        session.get.return_value = response

        async def mock_response_content():
            return ["line 1", "line 2"]

        response.content = mock_response_content()

        conn = aiohttp.UnixConnector(path="/var/run/docker.sock")
        async with aiohttp.ClientSession(connector=conn) as session:
            async with session.get(f"http://xx/containers/{cont}/logs?follow=1&stdout=1") as resp:
                async for line in resp.content:
                    self.assertIn(line, ["line 1", "line 2"])

    async def test_logs_parameters(self):
        conn = aiohttp.UnixConnector(path="/var/run/docker.sock")
        async with aiohttp.ClientSession(connector=conn) as session:
            async with session.get(f"http://xx/containers/{cont}/logs?follow=1&stdout=1") as resp:
                self.assertEqual(resp.url, f"http://xx/containers/{cont}/logs?follow=1&stdout=1")

    async def test_logs_print(self):
        conn = aiohttp.UnixConnector(path="/var/run/docker.sock")
        async with aiohttp.ClientSession(connector=conn) as session:
            async with session.get(f"http://xx/containers/{cont}/logs?follow=1&stdout=1") as resp:
                async for line in resp.content:
                    print_output = f"{name} {line}"
                    self.assertEqual(print_output, f"{name} {line}")
