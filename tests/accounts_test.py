import pytest

def test_user_is_logged_in(client):
    # Login the user
    response = client.post("/login/", data={"username": "test_user", "password": "test_password"})  # Note the trailing slash


    # Ensure the login was successful
    assert response.status_code in [200, 302]  # It might redirect after login

    # Assert that the user is logged in
    response = client.get("/me")
    assert response.status_code == 200
    # Assuming the response contains a JSON object with the username
    assert response.json()["username"] == "test_user"

