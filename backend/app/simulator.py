"""Synthetic network traffic data for the NetScope demo API."""

from datetime import datetime, timedelta, timezone
import random


def current_sample() -> dict:
    download = round(random.uniform(18.0, 115.0), 2)
    upload = round(random.uniform(4.0, 42.0), 2)
    tcp_packets = random.randint(500, 3200)
    udp_packets = random.randint(250, 1900)
    total_packets = tcp_packets + udp_packets

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "download_mbps": download,
        "upload_mbps": upload,
        "total_mbps": round(download + upload, 2),
        "total_packets": total_packets,
        "active_connections": random.randint(12, 86),
        "protocols": {
            "tcp": {"packets": tcp_packets, "percentage": round(tcp_packets / total_packets * 100, 1)},
            "udp": {"packets": udp_packets, "percentage": round(udp_packets / total_packets * 100, 1)},
        },
    }


def history_samples(points: int = 30) -> list[dict]:
    now = datetime.now(timezone.utc)
    samples = []
    for index in range(points):
        offset = points - index - 1
        sample = current_sample()
        sample["timestamp"] = (now - timedelta(seconds=5 * offset)).isoformat()
        samples.append(sample)
    return samples
