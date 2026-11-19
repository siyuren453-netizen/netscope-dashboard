# NetScope — Real-Time Network Traffic Dashboard

NetScope is a learning-focused network traffic monitoring and visualization dashboard for network engineering students, developers, and technology enthusiasts. The initial release uses **simulated traffic data**; it does not capture or inspect traffic from a real network interface.

## Features

- FastAPI backend exposing traffic summary and time-series endpoints.
- React, TypeScript, Vite, and Tailwind CSS frontend with a responsive dark interface.
- ECharts visualizations for recent traffic trends and TCP/UDP protocol distribution.
- Periodic polling of the API to make the simulated dashboard update in real time.
- Basic backend API tests with pytest.

## Project structure

```text
netscope-dashboard/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── simulator.py
│   └── tests/
│       └── test_api.py
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── postcss.config.js
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── src/
│       ├── App.tsx
│       ├── index.css
│       ├── main.tsx
│       └── types.ts
├── .gitignore
└── requirements.txt
```

## Requirements

- Python 3.10 or later
- Node.js 18 or later and npm

## Run locally

Open two terminals from the repository root.

### 1. Start the API

```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --app-dir backend --reload
```

The API is available at <http://localhost:8000>. Interactive API documentation is at <http://localhost:8000/docs>.

### 2. Start the dashboard

```bash
cd frontend
npm install
npm run dev
```

Open the local URL printed by Vite (normally <http://localhost:5173>). The Vite development server forwards `/api` requests to the FastAPI server on port 8000.

## API endpoints

- `GET /api/health` — basic service status.
- `GET /api/traffic/summary` — current simulated throughput, packet count, connection count, and TCP/UDP split.
- `GET /api/traffic/history?points=30` — simulated recent download and upload samples. `points` is limited to 2–120.

All rates are expressed in Mbps. The values are generated for demonstration and should not be interpreted as measurements from a live network.

## Tests

From the repository root, install the Python dependencies and run:

```bash
pytest backend/tests
```

The tests exercise the summary and history API responses using FastAPI's test client. Tests have been added, but no claim is made here that they have been run in this environment.

## Current limitations

This version generates synthetic values in the backend. It does not open a network interface, capture packets, persist metrics, authenticate users, or provide alerting. The dashboard polls the API every five seconds; it does not use a WebSocket stream.

## Roadmap: real packet capture

A future, separate capture component is planned in **Rust**, using **libpcap** on supported Unix-like systems and **Npcap** on Windows. The intended development path is:

1. Build a Rust capture service with explicit interface selection and configurable capture filters.
2. Aggregate packet metadata (such as timestamps, protocol, and byte counts) without retaining payloads by default.
3. Add permission checks, clear consent and privacy documentation, and safe handling of capture privileges.
4. Expose aggregated metrics to the FastAPI service through a documented local interface.
5. Keep the simulator available for demos and tests when packet capture is unavailable.

This is a roadmap only; Rust capture and libpcap/Npcap integration are **not implemented** in the current version. Capturing traffic may require elevated privileges and must only be done on networks and interfaces you are authorized to monitor.

## Development notes

The API and frontend are intentionally separated. The simulator can later be replaced behind the API boundary, while the dashboard continues to consume the same response shapes.
