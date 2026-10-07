# FDE Week 1 HW – Invoice API

This is a small invoice API built with FastAPI.

In class, the invoices were kept in Python memory, so they were lost when the server stopped. In this homework, the invoices are saved in a file called `invoices.json`. Now the data is still there after we restart the server.

Flow: Client / Swagger -> FastAPI -> Python code -> `invoices.json`

## Links

- API base URL: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs

## API endpoints

| Method | Path | What it does | Success | Errors |
|---|---|---|---|---|
| GET | `/invoices` | Get all invoices | 200 | – |
| GET | `/invoices/{invoice_id}` | Get one invoice | 200 | 404 if not found |
| POST | `/invoices` | Add a new invoice | 201 | 409 if the id already exists, 422 if the data is wrong |
| DELETE | `/invoices/{invoice_id}` | Delete an invoice | 200 | 404 if not found |

## Invoice fields

| Field | Type | Required | Default |
|---|---|---|---|
| `invoice_id` | text | yes | – |
| `vendor` | text | yes | – |
| `amount` | number | yes | – |
| `status` | text | no | `"PENDING"` |

Example for `POST /invoices`:

```json
{
  "invoice_id": "INV-103",
  "vendor": "Acme Inc",
  "amount": 50000,
  "status": "PENDING"
}
```

Starting data in `invoices.json`:

```json
[
  { "invoice_id": "INV-101", "vendor": "ABC Ltd",  "amount": 85000,  "status": "PENDING" },
  { "invoice_id": "INV-102", "vendor": "XYZ Corp", "amount": 142500, "status": "PENDING" }
]
```

## How it works

- `load_invoices()` reads the invoices from the JSON file.
- `save_invoices()` writes the invoices back to the JSON file.
- Every endpoint reads from the file, so the file is always the source of truth.

## Check that data is saved after restart

1. Open http://127.0.0.1:8000/docs.
2. Use `POST /invoices` to add a new invoice, for example `INV-103`.
3. Stop the server (Ctrl+C) and start it again.
4. Use `GET /invoices`. The new invoice is still there.
5. Use `DELETE /invoices/INV-103` to clean up.
