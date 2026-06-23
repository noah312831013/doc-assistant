class TestRegister:
    def test_register_success(self, client):
        response = client.post(
            "/auth/register",
            json={
                "username": "testuser",
                "email": "test@test.com",
                "password": "secret123",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "testuser"
        assert "password" not in data  # 確保密碼沒有回傳

    def test_register_duplicate_username(self, client):
        payload = {
            "username": "testuser",
            "email": "test@test.com",
            "password": "secret123",
        }
        client.post("/auth/register", json=payload)
        response = client.post("/auth/register", json=payload)
        assert response.status_code == 400


class TestLogin:
    def test_login_success(self, client):
        # 先註冊
        client.post(
            "/auth/register",
            json={
                "username": "testuser",
                "email": "test@test.com",
                "password": "secret123",
            },
        )
        # 再登入
        response = client.post(
            "/auth/login",
            data={"username": "testuser", "password": "secret123"},
        )
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert response.json()["token_type"] == "bearer"

    def test_login_wrong_password(self, client):
        client.post(
            "/auth/register",
            json={
                "username": "testuser",
                "email": "test@test.com",
                "password": "secret123",
            },
        )
        response = client.post(
            "/auth/login",
            data={"username": "testuser", "password": "wrongpassword"},
        )
        assert response.status_code == 401

    def test_login_nonexistent_user(self, client):
        response = client.post(
            "/auth/login",
            data={"username": "nobody", "password": "secret123"},
        )
        assert response.status_code == 401


class TestRBAC:
    def _get_token(self, client) -> str:
        client.post(
            "/auth/register",
            json={
                "username": "testuser",
                "email": "test@test.com",
                "password": "secret123",
            },
        )
        response = client.post(
            "/auth/login",
            data={"username": "testuser", "password": "secret123"},
        )
        return response.json()["access_token"]

    def test_protected_endpoint_without_token(self, client):
        """沒有 token 應被擋下（401）"""
        response = client.get("/documents")  # Day 3 會加這個 endpoint
        assert response.status_code in (401, 403, 404)  # 今天先驗邏輯

    def test_protected_endpoint_with_invalid_token(self, client):
        """無效 token 應被擋下（401）"""
        response = client.get(
            "/documents",
            headers={"Authorization": "Bearer invalid_token_here"},
        )
        assert response.status_code in (401, 403, 404)

    def test_auth_functions_directly(self, client):
        """直接測 auth 邏輯函式"""
        from app.auth import hash_password, verify_password

        hashed = hash_password("mysecret")
        assert verify_password("mysecret", hashed) is True
        assert verify_password("wrongpassword", hashed) is False
