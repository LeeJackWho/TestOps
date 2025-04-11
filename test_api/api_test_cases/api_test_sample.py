import pytest
from ..api.api_base import APIBase

def api_test_sample_api(base_url, api_session):
    api = APIBase(base_url, api_session)
    
    # 示例GET请求测试
    response = api.get("/endpoint")
    assert response.status_code == 200
    
    # 示例POST请求测试
    data = {"key": "value"}
    response = api.post("/endpoint", json=data)
    assert response.status_code == 201