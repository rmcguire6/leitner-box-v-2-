from app import schemas
from .database import client, session

def test_root(client):
  res = client.get("/")
  print(res.json().get("message"))
  assert res.json().get("message") == 'Welcome to Leitner Box'

def test_create_user(client):
  res = client.post("/users/", json={
    "email": "abby@example.com",
    "username": "Abby",
    "cards_per_day": 3,
    "password": "123pass"
    })
  new_user = schemas.UserOut(**res.json())
  assert new_user.email == 'abby@example.com'
  assert res.status_code == 201