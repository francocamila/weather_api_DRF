#Unity test

import pytest
from app.utils import fetch_weather

def test_if_weather_returns_data(monkeypatch):
    class MockResponse:
        def json(self):
            return {
    "source": "api",
    "data": "céu limpo"
}
        def raise_for_status(self):
            pass
    
    def mock_get(*args, **kwargs):
        return MockResponse()
    
    monkeypatch.setattr("requests.get", mock_get)
    result = fetch_weather("Brasília")
    assert result["data"] =="céu limpo"