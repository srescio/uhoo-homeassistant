"""Global fixtures for uHoo integration."""

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component
from pyuhoo.device import Device
from pyuhoo.errors import UnauthorizedError
from unittest.mock import patch
from .const import MOCK_DEVICE, MOCK_DEVICE_DATA

pytest_plugins = "pytest_homeassistant_custom_component"


@pytest.fixture
async def hass() -> HomeAssistant:
    """Set up a Home Assistant instance for testing."""
    hass = HomeAssistant()
    await async_setup_component(hass, "homeassistant", {})
    await hass.async_block_till_done()
    return hass


@pytest.fixture
async def enable_custom_integrations(hass: HomeAssistant) -> None:
    """Enable custom integrations defined in the test dir."""
    await hass.async_add_executor_job(hass.data.pop, loader.DATA_CUSTOM_COMPONENTS)


# This fixture is used to prevent HomeAssistant from attempting to create and dismiss persistent
# notifications. These calls would fail without this fixture since the persistent_notification
# integration is never loaded during a test.
@pytest.fixture(name="skip_notifications", autouse=True)
def skip_notifications_fixture():
    """Skip notification calls."""
    with patch("homeassistant.components.persistent_notification.async_create"), patch(
        "homeassistant.components.persistent_notification.async_dismiss"
    ):
        yield


@pytest.fixture(name="bypass_async_setup_entry")
def bypass_async_setup_entry_fixture():
    with patch("custom_components.uhoo.async_setup_entry", return_value=True):
        yield


@pytest.fixture(name="mock_device")
def mock_device_fixture() -> Device:
    device = Device(MOCK_DEVICE)
    device.update_data(MOCK_DEVICE_DATA)
    return device


@pytest.fixture(name="bypass_login")
def bypass_login_fixture():
    with patch("custom_components.uhoo.Client.login"):
        yield


@pytest.fixture(name="error_on_login")
def error_login_fixture():
    with patch("custom_components.uhoo.Client.login", side_effect=UnauthorizedError):
        yield


@pytest.fixture(name="bypass_get_latest_data")
def bypass_get_lastest_data_fixture():
    with patch("custom_components.uhoo.Client.get_latest_data"):
        yield


@pytest.fixture(name="bypass_get_devices")
def bypass_get_devices_fixture(mock_device):
    devices = {mock_device.serial_number: mock_device}
    with patch("custom_components.uhoo.Client.get_devices", return_value=devices):
        yield
