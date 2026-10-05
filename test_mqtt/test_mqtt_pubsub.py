"""MQTT 发布/订阅核心用例：连接、回路、遗留消息、QoS、通配符"""
import pytest

from Common.read_file import load_yaml
from test_mqtt.mqtt.mqtt_base import MQTTBase

pytestmark = pytest.mark.mqtt


@pytest.fixture(scope="module")
def mqtt_data():
    return load_yaml("mqtt_data.yaml")["mqtt"]


def test_connect_and_disconnect(broker_host, broker_port):
    client = MQTTBase(broker_host, broker_port)
    client.connect()
    assert client.is_connected
    client.disconnect()


def test_pubsub_roundtrip(mqtt_client, mqtt_data):
    """数据驱动：每个 {topic, payload, qos} 组合做一次发布→订阅回路"""
    for case in mqtt_data["roundtrip"]:
        mqtt_client.subscribe(case["topic"], qos=case["qos"])
        mqtt_client.publish(case["topic"], case["payload"], qos=case["qos"])
        msg = mqtt_client.wait_message(timeout=5)
        assert msg is not None, f"未收到消息: {case['topic']}"
        assert msg.topic == case["topic"]
        assert msg.payload.decode("utf-8") == case["payload"]


def test_retained_message(broker_host, broker_port, mqtt_client, mqtt_data):
    """新订阅者应立即收到 retained 消息"""
    case = mqtt_data["retained"]
    mqtt_client.publish(case["topic"], case["payload"], retain=True)

    late_sub = MQTTBase(broker_host, broker_port).connect()
    try:
        late_sub.subscribe(case["topic"])
        msg = late_sub.wait_message(timeout=5)
        assert msg is not None, "retained 消息未被新订阅者接收"
        assert msg.payload.decode("utf-8") == case["payload"]
        assert msg.retain
    finally:
        # 清理遗留消息，避免污染后续运行
        mqtt_client.publish(case["topic"], "", retain=True)
        late_sub.disconnect()


def test_wildcard_subscription(mqtt_client, mqtt_data):
    """+ 单层通配符应匹配任意一级 topic"""
    case = mqtt_data["wildcard"]
    mqtt_client.subscribe(case["sub_topic"])
    mqtt_client.publish(case["pub_topic"], case["payload"], qos=1)
    msg = mqtt_client.wait_message(timeout=5)
    assert msg is not None, "通配符订阅未收到消息"
    assert msg.topic == case["pub_topic"]
