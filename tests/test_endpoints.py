from fastapi.testclient import TestClient
from api.v1.auth_v1 import app




client = TestClient(app=app)



def test_login_response_401():
    payload = {
        "email": "user@example.com",
        "password": "12345i6i6rjj"
    }
    response = client.post("AuthService/login", json=payload)
    assert response.status_code == 401


# def test_me_endpoint():
#     response = client.post("AuthService/me")
#     assert response.status_code == 200


