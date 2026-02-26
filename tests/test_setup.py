import importlib
import sys
import types
import unittest
from unittest import mock


class FakeRadio:
    def __init__(self):
        self.connected = None
        self.ipv4_address = "192.168.1.10"

    def connect(self, ssid, password):
        self.connected = (ssid, password)

    def ping(self, ipv4):
        return 0.015


class FakeSession:
    def __init__(self, pool, context):
        self.pool = pool
        self.context = context


class FakeSocketPool:
    def __init__(self, radio):
        self.radio = radio


class TestSetup(unittest.TestCase):
    def setUp(self):
        self.fake_wifi = types.ModuleType("wifi")
        self.fake_wifi.radio = FakeRadio()

        self.fake_socketpool = types.ModuleType("socketpool")
        self.fake_socketpool.SocketPool = FakeSocketPool

        self.fake_requests = types.ModuleType("adafruit_requests")
        self.fake_requests.Session = FakeSession

        self.fake_secrets = types.ModuleType("secrets")
        self.fake_secrets.secrets = {"ssid": "MySSID", "password": "MyPassword"}

    def _load_setup_module(self):
        if "setup" in sys.modules:
            del sys.modules["setup"]
        return importlib.import_module("setup")

    def test_connect_to_wifi_uses_secrets(self):
        with mock.patch.dict(
            sys.modules,
            {
                "wifi": self.fake_wifi,
                "socketpool": self.fake_socketpool,
                "adafruit_requests": self.fake_requests,
                "secrets": self.fake_secrets,
            },
            clear=False,
        ):
            setup_module = self._load_setup_module()
            result = setup_module.connect_to_wiFi(magtag=object())

        self.assertIs(result, self.fake_wifi)
        self.assertEqual(self.fake_wifi.radio.connected, ("MySSID", "MyPassword"))

    def test_setup_requests_creates_session_with_socket_pool(self):
        with mock.patch.dict(
            sys.modules,
            {
                "wifi": self.fake_wifi,
                "socketpool": self.fake_socketpool,
                "adafruit_requests": self.fake_requests,
                "secrets": self.fake_secrets,
            },
            clear=False,
        ):
            setup_module = self._load_setup_module()
            with mock.patch.object(setup_module.ssl, "create_default_context", return_value="CTX"):
                session = setup_module.setup_requests()

        self.assertIsInstance(session, FakeSession)
        self.assertIsInstance(session.pool, FakeSocketPool)
        self.assertIs(session.pool.radio, self.fake_wifi.radio)
        self.assertEqual(session.context, "CTX")


if __name__ == "__main__":
    unittest.main()
