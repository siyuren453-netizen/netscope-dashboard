from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint_reports_ok():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_summary_contains_simulated_rates_and_protocols():
    response = client.get("/api/traffic/summary")
    assert response.status_code == 200
    data = response.json()
    assert 18 <= data["download_mbps"] <= 115
    assert 4 <= data["upload_mbps"] <= 42
    assert data["total_mbps"] == round(data["download_mbps"] + data["upload_mbps"], 2)
    assert set(data["protocols"]) == {"tcp", "udp"}
    assert data["total_packets"] == sum(protocol["packets"] for protocol in data["protocols"].values())


def test_history_returns_requested_number_of_samples():
    response = client.get("/api/traffic/history?points=8")
    assert response.status_code == 200
    samples = response.json()["samples"]
    assert len(samples) == 8
    assert all("download_mbps" in sample and "upload_mbps" in sample for sample in samples)


def test_history_rejects_out_of_range_points():
    response = client.get("/api/traffic/history?points=1")
    assert response.status_code == 422
