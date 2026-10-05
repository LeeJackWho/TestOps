"""MQTT 测试夹具：broker 地址从环境变量读取，默认本机 Mosquitto"""
import os

import pytest

from test_mqtt.mqtt.mqtt_base import MQTTBase


@pytest.fixture(scope="session")
def broker_host() -> str:
    return os.getenv("MQTT_BROKER", "localhost")


@pytest.fixture(scope="session")
def broker_port() -> int:
    return int(os.getenv("MQTT_PORT", "1883"))


@pytest.fixture
def mqtt_client(broker_host, broker_port):
    """函数级客户端，用完自动断开"""
    client = MQTTBase(broker_host, broker_port)
    client.connect()
    yield client
    client.disconnect()
