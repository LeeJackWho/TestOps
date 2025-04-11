import requests
from typing import Dict, Any

class APIBase:
    def __init__(self, base_url: str, session: requests.Session):
        self.base_url = base_url
        self.session = session

    def get(self, path: str, params: Dict = None) -> requests.Response:
        url = f"{self.base_url}{path}"
        return self.session.get(url, params=params)

    def post(self, path: str, json: Dict = None) -> requests.Response:
        url = f"{self.base_url}{path}"
        return self.session.post(url, json=json)

    def put(self, path: str, json: Dict = None) -> requests.Response:
        url = f"{self.base_url}{path}"
        return self.session.put(url, json=json)

    def delete(self, path: str) -> requests.Response:
        url = f"{self.base_url}{path}"
        return self.session.delete(url)