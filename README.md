# FDE Week 1 – Invoice API (JSON Persistence)

A small FastAPI service for managing invoices. Invoice data is stored in a JSON file
(`src/invoice_api/data/invoices.json`) instead of Python memory, so **data survives a server restart**.

```
Client / Swagger -> FastAPI -> Python logic -> invoices.json
```

## Project structure

```
src/invoice_api/
├── main.py                 # FastAPI app (GET, POST, DELETE + load/save helpers)
└── data/
    └── invoices.json       # persisted invoice data
```

## Setup & run

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install fastapi uvicorn

cd src\invoice_api          # must run from this folder (data path is relative)
uvicorn main:app --reload
```

- API base URL: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- OpenAPI schema: http://127.0.0.1:8000/openapi.json

## API endpoints (from `/docs`)

| Method | Path | Description | Success | Errors |
|---|---|---|---|---|
| GET | `/invoices` | List all invoices (read from `invoices.json`) | 200 | – |
| GET | `/invoices/{invoice_id}` | Get one invoice | 200 | 404 not found |
| POST | `/invoices` | Create an invoice and save it to the file | 201 | 409 duplicate id, 422 validation |
| DELETE | `/invoices/{invoice_id}` | Delete an invoice and save the file | 200 | 404 not found, 422 validation |

### Invoice schema

| Field | Type | Required | Default |
|---|---|---|---|
| `invoice_id` | string | yes | – |
| `vendor` | string | yes | – |
| `amount` | number | yes | – |
| `status` | string | no | `"PENDING"` |

Example request body for `POST /invoices`:

```json
{
  "invoice_id": "INV-103",
  "vendor": "Acme Inc",
  "amount": 50000,
  "status": "PENDING"
}
```

Seed data (`invoices.json`):

```json
[
  { "invoice_id": "INV-101", "vendor": "ABC Ltd",  "amount": 85000,  "status": "PENDING" },
  { "invoice_id": "INV-102", "vendor": "XYZ Corp", "amount": 142500, "status": "PENDING" }
]
```

## How it works

- `load_invoices()` reads the file with `json.load()`.
- `save_invoices()` writes the list back with `json.dump()`.
- Every endpoint calls `load_invoices()` first, so the file is the single source of truth.

## Proving persistence

1. Start the server and open http://127.0.0.1:8000/docs.
2. `POST /invoices` with a new invoice (e.g. `INV-103`).
3. Stop Uvicorn (Ctrl+C) and start it again.
4. `GET /invoices` – the new invoice is still returned, and it is visible in `invoices.json`.
5. `DELETE /invoices/INV-103` to clean up.

## Scope

Core: GET + POST + DELETE with JSON persistence. PUT (update) is a possible bonus; PostgreSQL is not required.
