# TradeFlow — Event-Driven Automated Trading Platform

An event-driven, microservices-lite algorithmic trading system engineered for high-reliability equity trading in Indian markets. Built with decoupled worker processes, TimescaleDB time-series persistence, Redis pub/sub event bus, strict risk controls, and a Next.js real-time telemetry command center.

---

## 🏛️ Architecture Overview

The system decouples data ingestion, quantitative signal generation, and order execution into independent runtimes. A failure in the UI or web server cannot disrupt trade management, and data feed spikes cannot block risk enforcement.

```
                    ┌─────────────────────────────────────────┐
                    │           Market Feed / Broker          │
                    └────────────────────┬────────────────────┘
                                         │ WebSocket / Polling
                                         ▼
                    ┌─────────────────────────────────────────┐
                    │            Ingestion Worker             │
                    │  (Candle Aggregation & Validation)      │
                    └──────────┬──────────────────┬───────────┘
                               │                  │
                OHLCV Hypertable                  │ Redis Pub/Sub
                               ▼                  ▼
                    ┌──────────────────┐   ┌──────────────────────────┐
                    │   TimescaleDB    │   │     Redis Event Bus      │
                    │  (Time-Series)   │   │   (market.candle.closed) │
                    └──────────────────┘   └─────────────┬────────────┘
                                                         │
                                                         ▼
                                           ┌──────────────────────────┐
                                           │       Logic Worker       │
                                           │ (40+ Indicators & Strats)│
                                           └─────────────┬────────────┘
                                                         │
                                             Redis Signal│ (signal.generated)
                                                         ▼
                                           ┌──────────────────────────┐
                                           │     Execution Worker     │
                                           │  ├── Risk Engine         │
                                           │  ├── Position Sizing     │
                                           │  ├── MTM Circuit Breaker │
                                           │  └── Broker Adapter      │
                                           └─────────────┬────────────┘
                                                         │
                                         Order Execution │ (Paper / Live)
                                                         ▼
                                           ┌──────────────────────────┐
                                           │   FastAPI + WebSockets   │
                                           └─────────────┬────────────┘
                                                         │
                                                         ▼
                                           ┌──────────────────────────┐
                                           │   Next.js Command Center │
                                           │ (Real-time P&L & Audits) │
                                           └──────────────────────────┘
```

---

## ⚡ Key Highlights

### 1. Isolated Worker Architecture
- **`ingestion_worker`**: Streams tick data, constructs standardized time-frame candles, handles gap filling, and writes directly into TimescaleDB hypertables while broadcasting on Redis.
- **`logic_worker`**: Consumes closed candles from Redis, calculates technical indicators, evaluates active strategies (ORB, Mean Reversion, Breakouts), and generates validated signal events.
- **`execution_worker`**: The **sole** process authorized to place or modify orders. Operates behind strict safety gates (position limits, MTM drawdown caps, daily kill switch).

### 2. Time-Series Optimized Persistence
- Backed by **TimescaleDB** (PostgreSQL extension optimized for fast time-series analytical queries).
- Automated partitioning into hypertables for sub-millisecond retrieval of multi-timeframe OHLCV bars.

### 3. Institutional Risk Engine & Circuit Breakers
- **Hard Kill Switch**: Immediate shutdown on abnormal market conditions or API anomalies.
- **MTM Drawdown Guard**: Blocks all new order submissions if intraday unrealized loss exceeds `MAX_DAILY_DRAWDOWN_PCT`.
- **Position Sizing Engine**: Strict dynamic allocation (e.g. 1% capital at risk per trade) factoring volatility and stop-loss distance.
- **Pluggable Broker Interface**: All execution runs through `BrokerBase` with **Paper Trading** enabled by default for zero-capital verification.

### 4. Real-Time Telemetry Dashboard
- Built with **Next.js 14**, **Tailwind CSS**, and **WebSockets**.
- Live P&L tracking, open positions, active signal feed, execution logs, and worker health heartbeats.

---

## 🛠️ Tech Stack

| Domain | Technologies |
|---|---|
| **Backend & Workers** | Python 3.11+, FastAPI, Pydantic v2, AsyncIO |
| **Event Bus & Caching**| Redis 7 (Pub/Sub & streams) |
| **Database** | TimescaleDB / PostgreSQL 16 |
| **Frontend** | Next.js 14, React, Tailwind CSS, Lucide Icons |
| **Infra & DevOps** | Docker Compose, Pytest |

---

## 📂 Project Structure

```
├── backend/
│   ├── app/
│   │   ├── alerts/          # Telegram alerts & incident notifications
│   │   ├── api/             # FastAPI REST endpoints & WebSocket handlers
│   │   ├── broker/          # Broker abstraction layer (Paper & Live adapters)
│   │   ├── core/            # Config, database connection, Redis event bus
│   │   ├── risk/            # RiskEngine, MTM limits, position sizer
│   │   ├── services/        # Vectorized indicator engine
│   │   ├── strategies/      # Strategy registry & base implementations
│   │   └── workers/         # Ingestion, Logic, and Execution workers
│   └── tests/               # Unit & integration test suites
├── frontend/
│   ├── app/                 # Next.js App Router (dashboard pages)
│   └── components/          # Real-time metrics, active orders, signals, charts
├── infra/
│   └── timescaledb/         # Schema initialization and hypertables SQL
└── docker-compose.yml       # TimescaleDB & Redis container orchestration
```

---

## 🚀 Quick Start

### 1. Start Infrastructure
```bash
docker compose up -d
```
Starts TimescaleDB on `:5432` and Redis on `:6379`.

### 2. Configure Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e ".[dev]"
cp ../.env.example .env
```

### 3. Run FastAPI Gateway
```bash
uvicorn app.main:app --reload --port 8000
```

### 4. Start Background Workers (Separate Terminals)
```bash
# Terminal 1: Ingestion
python -m app.workers.ingestion_worker

# Terminal 2: Strategy Logic
python -m app.workers.logic_worker

# Terminal 3: Order Execution & Risk Engine
python -m app.workers.execution_worker
```

### 5. Launch Dashboard UI
```bash
cd frontend
npm install
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) to view the live trading command center.

---

## 🔒 Safety & Production Defaults

- **Paper Trading Default**: Safe out-of-the-box sandbox execution.
- **Fail-Safe Sizing**: Orders rejected if position size exceeds permissible capital thresholds.
- **Health Heartbeats**: Every worker reports its health status via Redis key TTLs to flag degraded pipelines immediately.
