from fastapi.testclient import TestClient
from main import app

def run_test():
    client = TestClient(app)
    resp = client.get("/")
    print(resp.status_code)
    print(resp.json())

if __name__ == "__main__":
    run_test()
