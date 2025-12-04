# Gemini Context: DeliveryBot Project (v1)

This file provides context, architectural guidelines, and operational instructions for the **DeliveryBot** project.

## 1. Project Overview

**DeliveryBot** is a modular chatbot architecture designed to process WhatsApp messages via Mega API.
The system operates as a Full-Cycle Pipeline: **Ingestion -> Cleaning -> Thinking (AI) -> Response**.

*   **Tech Stack:** Python 3.10+, FastAPI, LangGraph, LangChain.
*   **AI Provider:** Google Gemini (Model: `gemini-2.5-flash-preview-09-2025`).
*   **Integration:** Mega API (WhatsApp) + Ngrok (Tunneling).

## 2. Architecture & Flow

The project is split into two distinct layers:

1.  **Ingestion Layer (Server):**
    *   **File:** `src/server/webhook_server.py`
    *   **Role:** "Agnostic Sponge". Receives raw JSON from Mega API, logs it, triggers the robot, and returns `200 OK`.
2.  **Logic Layer (LangGraph Workflow):**
    *   **`main.py`:** The Workflow Orchestrator (with `MemorySaver` persistence).
    *   **`node_base_field.py`:** Data Cleaner (Extracts phone/message).
    *   **`node_agente_AI.py`:** The Brain. Reads persona from `prompt.md`, queries Gemini, logs conversation to `node_historico.log`.
    *   **`node_responder_cliente.py`:** The Postman (Sends response back via Mega API).

## 3. Directory Structure

```text
projeto_v1/
├── .env_local                 # Environment variables (API Keys) - RENAMED for security
├── .gitignore                 # Specifies intentionally untracked files (e.g., .env_local, logs)
├── main.py                    # LangGraph definition
├── requirements.txt           # Python dependencies
├── guia_instalacao.md         # Detailed installation and setup guide
├── src/
│   ├── state.py               # Data Schema (TypedDict)
│   ├── server/
│   │   ├── webhook_server.py  # Ingestion server
│   │   └── guia_servidor.md   # Server docs
│   └── nodes/                 # Business Logic
│       ├── node_base_field.py       # JSON Parser
│       ├── node_agente_AI.py        # AI Logic
│       ├── node_responder_cliente.py # API Sender
│       ├── prompt.md                # AI Persona Configuration
│       └── node_historico.log       # Conversation Logs (Auto-generated)
```

## 4. Setup & Execution Guide

### A. Environment Setup
```bash
cd ~/Desktop/projeto_v1
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### B. Running the Server
```bash
python3 src/server/webhook_server.py
```
*Server runs at `http://0.0.0.0:8000`.*

### C. Exposing to Internet (Ngrok)
**Authentication is mandatory.**
```bash
ngrok http 8000
```

### D. Mega API Configuration
*   **Webhook URL:** `https://<your-ngrok-url>/webhook`
*   **Triggers:** `on_message`

## 5. Key Features

### 🧠 Dynamic AI Persona
To change the bot's behavior, simply edit `src/nodes/prompt.md`. No code changes required.

### 📝 Logging
All conversations are automatically saved to `src/nodes/node_historico.log` for auditing.

### 🔐 Security
*   Keys stored in `.env_local`. **Ensure `.env_local` and `src/nodes/node_historico.log` are listed in `.gitignore` to prevent accidental commits.**
*   Code uses conditional imports for AI drivers.

## 6. Coding Conventions

### Node Naming in Graph (`main.py`)
When adding nodes to `workflow.add_node(...)`, always remove the `node_` prefix from the string identifier.
**Pattern:** `workflow.add_node("suffix_name", node_function_name)`

**Examples:**
*   ✅ `workflow.add_node("base_field", node_base_field)`
*   ✅ `workflow.add_node("agente_ai", node_agente_ai)`
*   ✅ `workflow.add_node("responder_cliente", node_responder_cliente)`
*   ❌ `workflow.add_node("node_base_field", node_base_field)` (Don't repeat 'node')

## 7. Troubleshooting

*   **Error 403 (Key Leaked):** Regenerate Google Key and update `.env_local`.
*   **Error 404 (Model Not Found):** Update `langchain-google-genai` and check model name in `node_agente_AI.py`.
*   **No Response:** Check if Mega API URL has `https://`.
