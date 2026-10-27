import socket
import time
from prometheus_client import start_http_server, Gauge

TARGETS = [
    ("google", "google.com", 443),
    ("github", "github.com", 443),
    ("cloudflare-dns", "1.1.1.1", 53),
    ("grafana", "grafana", 3000),
    ("offline-demo", "example.invalid", 80),
]

UP = Gauge("target_up", "1 if the target is reachable", ["name"])
LATENCY = Gauge("target_latency_ms", "TCP connect time in ms", ["name"])

def check(host, port):
    start = time.time()
    try:
        with socket.create_connection((host, port), timeout=3):
            return 1, (time.time() - start) * 1000
    except OSError:
        return 0, 0

if __name__ == "__main__":
    start_http_server(8000)
    while True:
        for name, host, port in TARGETS:
            up, ms = check(host, port)
            UP.labels(name).set(up)
            LATENCY.labels(name).set(ms)
        time.sleep(10)
