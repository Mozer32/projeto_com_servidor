# Gemini Context: DeliveryBot Project (v1)

This file provides context, architectural guidelines, and operational instructions for the **DeliveryBot** project.

## 1. Project Overview

**DeliveryBot** is a modular chatbot architecture designed to process WhatsApp messages via Mega API.
The project is currently split into two distinct layers:

1.  **Ingestion Layer (Server):** A robust, agnostic FastAPI server that receives webhooks, logs the raw payload, and returns `200 OK`. It acts as a "sponge" to capture data without breaking on validation errors.
    *   **File:** `src/server/webhook_server.py`
    *   **Role:** Listen, Log, Confirm.
2.  **Logic Layer (LangGraph):** A stateful workflow engine (using LangGraph) that will process the business logic (currently decoupled).

*   **Tech Stack:** Python 3.10+, FastAPI, Uvicorn, LangGraph, LangChain.
*   **Infrastructure:** Ngrok (Tunneling), Mega API (WhatsApp Provider).

## 2. Directory Structure

The project follows a clean separation of concerns in `projeto_v1/`:

```text
projeto_v1/
├── .env                       # Environment variables (API Keys)
├── main.py                    # LangGraph definition (Workflow engine)
├── requirements.txt           # Python dependencies
├── guia_instalacao.md         # Detailed installation and setup guide
├── src/
│   ├── state.py               # Data Schema (TypedDict) for the graph
│   ├── server/
│   │   └── webhook_server.py  # The ACTIVE ingestion server (FastAPI)
│   └── nodes/                 # Graph Nodes (Business Logic)
│       ├── node_atendente.py  # First processing node
│       └── ...
└── tests/                     # Test scripts
```

## 3. Setup & Execution Guide

### A. Environment Setup
Standard procedure to prepare the workspace:

```bash
cd ~/Desktop/projeto_v1
python3 -m venv venv
source venv/bin/activate  # Mac/Linux (Windows: venv\Scripts\activate)
pip install -r requirements.txt
```

### B. Ingestion Server (The "Sponge")
This is the primary entry point for webhooks. It listens on port 8000.

```bash
# From projeto_v1/ directory
python3 src/server/webhook_server.py
```
*Output indicates server running at `http://0.0.0.0:8000`.*

### C. Exposing to Internet (Ngrok)
To receive real messages from Mega API, a tunnel is required.

**1. Authentication (CRITICAL):**
To avoid "Browser Warning" blocks from Ngrok, you must authenticate:
```bash
# If using global install:
ngrok config add-authtoken <YOUR_TOKEN>

# If using local binary:
./ngrok config add-authtoken <YOUR_TOKEN>
```

**2. Start Tunnel:**
In a new terminal window (keep Python running in the other):
```bash
ngrok http 8000
```
*Copy the generated HTTPS link (e.g., `https://xxxx.ngrok-free.app`).*

### D. Configuring Mega API
1.  Access the Mega API panel.
2.  In the **Webhook** field, paste your Ngrok link **Appending the endpoint**:
    👉 `https://<your-ngrok-url>/webhook`
3.  Ensure triggers (e.g., `on_message`) are checked/active.
4.  Save changes.

## 4. Testing Flow

1.  **Send Message:** Send a WhatsApp message to the connected number.
2.  **Check Python Terminal:** You should see the raw JSON payload logged.
3.  **Check Ngrok Terminal:** You should see a `200 OK` request.

## 5. Development Conventions

*   **Server Philosophy:** The server (`webhook_server.py`) must remain **agnostic**. Do not add business logic there. It should only receive, log, and confirm.
*   **State Management:** All business data must flow through the `base_cliente_state` defined in `src/state.py`.
*   **Imports:** Run python modules from the root (`projeto_v1`) to avoid `ModuleNotFoundError`. Example: `python3 -m src.server.webhook_server`.

## 6. Current Status & Next Steps

*   **Completed:**
    *   Environment setup (`venv`).
    *   Dependency installation.
    *   Ingestion Server (`webhook_server.py`) is active and tested.
    *   Ngrok tunneling is configured and authenticated.
*   **In Progress:**
    *   Connecting the Ingestion Server to the LangGraph logic (`main.py`).
    *   Parsing the raw JSON payload into the structured `base_cliente_state`.