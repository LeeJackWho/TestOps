"""Paho-Mqtt 客户端封装：连接管理、发布/订阅、消息队列收取"""
import queue
import uuid
from typing import Optional

import paho.mqtt.client as mqtt


class MQTTBase:
    """基于 paho-mqtt 的测试客户端封装。

    典型用法：
        client = MQTTBase(host, port).connect()
        client.subscribe("testops/demo/topic1")
        client.publish("testops/demo/topic1", '{"soc": 85}', qos=1)
        msg = client.wait_message(timeout=5)
    """

    def __init__(self, host: str, port: int = 1883,
                 client_id: Optional[str] = None, keepalive: int = 60):
        self.host = host
        self.port = port
        self.keepalive = keepalive
        self._connected = False
        self._messages: "queue.Queue[mqtt.MQTTMessage]" = queue.Queue()
        self._client = mqtt.Client(
            client_id=client_id or f"testops-{uuid.uuid4().hex[:8]}")
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message

    # ---- paho 回调 ----
    def _on_connect(self, client, userdata, flags, rc):
        self._connected = (rc == 0)

    def _on_message(self, client, userdata, msg):
        self._messages.put(msg)

    # ---- 对外接口 ----
    @property
    def is_connected(self) -> bool:
        return self._connected

    def connect(self) -> "MQTTBase":
        rc = self._client.connect(self.host, self.port, self.keepalive)
        assert rc == mqtt.MQTT_ERR_SUCCESS, f"MQTT 连接失败, rc={rc}"
        self._client.loop_start()
        return self

    def subscribe(self, topic: str, qos: int = 0) -> None:
        result, _ = self._client.subscribe(topic, qos)
        assert result == mqtt.MQTT_ERR_SUCCESS, f"订阅失败: {topic}"

    def publish(self, topic: str, payload: str,
                qos: int = 0, retain: bool = False):
        info = self._client.publish(topic, payload, qos=qos, retain=retain)
        if qos > 0:
            info.wait_for_publish(timeout=10)
        assert info.rc == mqtt.MQTT_ERR_SUCCESS, f"发布失败: {topic}"
        return info

    def wait_message(self, timeout: float = 5.0) -> Optional[mqtt.MQTTMessage]:
        """阻塞等待下一条消息，超时返回 None"""
        try:
            return self._messages.get(timeout=timeout)
        except queue.Empty:
            return None

    def clear_messages(self) -> None:
        with self._messages.mutex:
            self._messages.queue.clear()

    def disconnect(self) -> None:
        self._client.loop_stop()
        self._client.disconnect()

    def __enter__(self) -> "MQTTBase":
        return self.connect()

    def __exit__(self, *exc) -> None:
        self.disconnect()
