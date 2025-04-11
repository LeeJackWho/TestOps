import pytest
import requests

@pytest.fixture(scope="session")
def base_url():
    return "https://api.example.com"  # 替换为实际的API基础URL

@pytest.fixture(scope="session")
def api_session():
    session = requests.Session()
    # 可以在这里设置通用的headers等
    session.headers.update({
        "Content-Type": "application/json"
    })
    yield session
    session.close()