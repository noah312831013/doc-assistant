from fastapi.testclient import TestClient
from app.main import app

# TestClient 是 FastAPI 內建的同步測試工具
# 底層用 httpx，不需要真的啟動 server
client = TestClient(app)


class TestHealthEndpoint:
    def test_health_returns_200(self):
        """健康檢查應回傳 200"""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_response_schema(self):
        """回應 body 應包含正確欄位"""
        response = client.get("/health")
        data = response.json()

        assert "status" in data
        assert "service" in data
        assert "timestamp" in data

    def test_health_status_is_ok(self):
        """status 欄位應為 'ok'"""
        response = client.get("/health")
        assert response.json()["status"] == "ok"

    def test_health_service_name(self):
        """service 名稱應正確"""
        response = client.get("/health")
        assert response.json()["service"] == "doc-assistant-backend"
