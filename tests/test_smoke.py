from app import create_app
def test_healthcheck():
    app = create_app()
    client = app.test_client()
    resp = client.get("/healthcheck")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["status"] == "ok"
def test_record_requires_filters():
    app = create_app()
    client = app.test_client()
    resp = client.get("/record")
    assert resp.status_code == 400
