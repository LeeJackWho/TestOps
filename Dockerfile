# TestOps 测试执行镜像：框架自测 + API/MQTT 测试
# UI 测试需要浏览器内核，建议在宿主机按 README 运行
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 默认执行框架自测 + MQTT 集成测试（配合 compose 中的 mosquitto 服务）
CMD ["pytest", "tests", "test_mqtt", "-v", "-o", "addopts="]
